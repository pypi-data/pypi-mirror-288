import datetime
import json
import os
import sys
from openai import OpenAI
import base64
from pdf2image import convert_from_path
from typing import List, Dict, Any
from PIL import Image


class ScreenplayPDFToJSON:
    """
    A class to convert screenplay PDF files to JSON format.
    """

    def __init__(self, api_key: str, skip_title_page: bool = True) -> None:
        """
        Initialize the class with the API key for OpenAI.

        :param api_key: The API key for OpenAI.
        :param skip_title_page: Whether to skip the title page of the screenplay PDF.
        """
        self.client = OpenAI(api_key=api_key)
        self.skip_title_page = skip_title_page
        self.model = "gpt-4o"
        self.prompt = """
        Attached is an image of a screenplay page. Extract JSON using the format explained by the following JSON example
        (note 'page' is always <pn>):
        <JSON example>
        [
            {
                "type": "dialogue",
                "name": "JOHN",
                "modifier": "(V.O.)",
                "content": "Hello, how are you?",
                "page": <pn>
            },
            {
                "type": "action",
                "content": "John walks into the room.",
                "page": <pn>
            },
            {
                "type": "dialogue",
                "name": "MARY",
                "parenthetical": "(smiling)",
                "content": "I'm good, thank you!",
                "page": <pn>
            },
            {
                "type": "dialogue",
                "name": "JOHN",
                "content": "That's great to hear.",
                "page": <pn>
            },
            {
                "type": "scene",
                "content": "INT. LIVING ROOM - DAY",
                "page": <pn>
            }
        ]
        </JSON example>
        Give the response in pure JSON with no pre-amble or post-text. Do not include the symbols ```
        """
        self.av_words_per_page = 200    # average words per script page
        # https://openai.com/api/pricing/
        self.input_cost = 5 / 1e6  # based on GPT-4o Jun 2024
        self.output_cost = 15 / 1e6   # based on GPT-4o Jun 2024
        self.visual_cost = 0.003825  # based on GPT-4o 1700 by 2200 image Jun 2024
        self.word_count_to_token_count = 1.5
        self.json_keys_per_page = 17   # number of keys in the JSON response per page - very approximate
        self.time_to_convert_page = 22  # average time to convert a page image to JSON in seconds - will be faster outside of peak hours and speed up as models improve

    def get_image_dimensions(self, image_path):
        with Image.open(image_path) as img:
            width, height = img.size
        return width, height

    def convert_pdf_to_images(self, pdf_filename: str, end_page: int = 999999,
                              verbose: bool = True) -> List[str]:
        """
        Convert the PDF pages to JPEG images.

        :param pdf_filename: The name of the PDF file.
        :param end_page: The last page to convert.
        :return: A list of image file paths.
        """
        image_files = []  # List to store image file paths
        image_dir = "images_" + os.path.basename(pdf_filename).split('.')[0]  # Directory to store images
        if not os.path.exists(image_dir):  # Create directory if it doesn't exist
            os.makedirs(image_dir)

        pages = convert_from_path(pdf_filename, 200)  # Convert PDF to images
        for p, page in enumerate(pages[:end_page]):  # Loop through each page up to end_page
            if self.skip_title_page and p == 0:  # Skip title page if flag is set
                print(f"Skipping page {p} as title page")
                continue
            image_filename = f'{image_dir}/{os.path.basename(pdf_filename)}_{p}.jpeg'  # Image file path
            page.save(image_filename, 'JPEG')  # Save the page as JPEG
            image_files.append(image_filename)  # Add the image file path to the list
            if verbose:
                print(f"Saved {image_filename}")

        return image_files

    def extract_text_from_image(self, image_file: str, page_number: int) -> str:
        """
        Use OpenAI to extract text from an image.

        :param image_file: The path to the image file.
        :param page_number: The page number.
        :return: The extracted text in JSON format.
        """
        prompt = self.prompt  # Get the prompt
        with open(image_file, "rb") as f:  # Open image file in binary mode
            image_data = f.read()
        image_data = base64.b64encode(image_data).decode('utf-8')  # Encode image to base64
        prompt_actual = prompt.replace("<pn>", str(page_number))  # Replace placeholder with page number
        start = datetime.datetime.now()  # Start timer for performance measurement
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_actual,
                            "response_format": "json",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": "data:image/jpeg;base64," + image_data, "detail": "high"},
                        }
                    ]
                }
            ]
        )
        end = datetime.datetime.now()  # End timer
        reply = response.choices[0].message.content  # Extract the text from the response
        print(f"Visual Transformer analysis of {image_file} completed in {end - start} seconds")
        return reply

    def write_json_to_file(self, json_filename: str, json_data: str, is_last_file: bool) -> None:
        """
        Write JSON data to a file.

        :param json_filename: The name of the JSON file.
        :param json_data: The JSON data to write.
        :param is_last_file: Flag to indicate if it's the last file.
        """
        json_data = json_data.replace("[", "")  # Remove leading square bracket
        if not is_last_file:
            json_data = json_data.replace("]", ",")  # Replace trailing square bracket with a comma
        else:
            json_data = json_data.replace("]", "")  # Remove trailing square bracket
        with open(json_filename, "a") as f:  # Append the JSON data to the file
            f.write(json_data)

    def cleanup_json_file(self, json_filename: str) -> None:
        """
        Clean up the JSON file formatting.

        :param json_filename: The name of the JSON file.
        """
        with open(json_filename, "r") as f:  # Open the JSON file in read mode
            data = json.load(f)
        with open(json_filename, "w") as f:  # Write formatted JSON data back to the file
            f.write(json.dumps(data, indent=4))

    def estimate_conversion_cost(self, pdf_filename: str, end_page: int = 999) -> float:
        """
        Estimate the cost of converting a PDF to JSON.

        :return: The estimated cost.
        """
        print(f"Estimating conversion cost for {pdf_filename}")
        image_files = self.convert_pdf_to_images(pdf_filename, end_page, verbose=False)  # Convert PDF to images
        est_cost = len(image_files) * (self.visual_cost +
                                       len(self.prompt.split()) * self.word_count_to_token_count * self.input_cost +
                                       (self.av_words_per_page * self.word_count_to_token_count +
                                        self.json_keys_per_page * self.word_count_to_token_count) * self.output_cost)
        directory = os.path.dirname(image_files[0])  # Get the directory of the image files
        # delete all images in the directory directory
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))
        os.rmdir(directory)  # Delete image directory
        return est_cost

    def convert(self, pdf_filename: str, end_page: int = 999999) -> List[Dict[str, Any]]:
        """
        Main method to convert PDF to JSON.

        :param pdf_filename: The name of the PDF file.
        :param end_page: The last page to convert.
        :return: The JSON data.
        """

        json_filename = os.path.basename(pdf_filename).split('.')[0] + ".json"  # JSON file path
        with open(json_filename, "w") as f:  # Create JSON file and write opening bracket
            f.write("[")

        image_files = self.convert_pdf_to_images(pdf_filename, end_page)  # Convert PDF to images
        page_number = 2 if len(image_files) > 0 and 'title' in image_files[0].lower() else 1  # Determine starting page number
        av_words_per_page = 200
        input_cost =5/1e6
        output_cost = 15/1e6
        visual_cost = 0.003825
        est_cost = len(image_files) * (visual_cost + len(self.prompt.split())*1.5*input_cost +
                                       (av_words_per_page*1.5+ 17*1.5)*output_cost)
        print(f"Estimated API cost for conversion: ${est_cost:.2f}")
        print(f"Estimated time for conversion at peak time: {len(image_files) * self.time_to_convert_page/60:.2f} minutes")
        #input("Press Enter to continue...")
        for i, image_file in enumerate(image_files):  # Loop through each image file
            print(f"Visual Transformer analysis on {image_file} started, dimensions {self.get_image_dimensions(image_file)}")
            #input("Press Enter to continue...")
            reply = self.extract_text_from_image(image_file, page_number)  # Extract text from image
            page_number += 1
            self.write_json_to_file(json_filename, reply, i == len(image_files) - 1)  # Write extracted text to JSON file
            #print("*" * 80)

        with open(json_filename, "a") as f:  # Write closing bracket to JSON file
            f.write("]")

        self.cleanup_json_file(json_filename)  # Clean up JSON file formatting

        with open(json_filename, "r") as f:  # Load JSON data from file
            data = json.load(f)

        directory = os.path.dirname(image_files[0])  # Get the directory of the image files
        # delete all images in the directory directory
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))
        os.rmdir(directory)  # Delete image directory

        return data  # Return JSON data

    @staticmethod
    def format_screenplay_experimental(data):
        """
        UNDOCUMENTED EXPERIMENTAL METHOD
        Format the screenplay json into a screenplay text.
        Doesn't save result.
        :param data: screenplay json data
        :return: screenplay text
        """
        screenplay_text = ""
        num_tabs_character = 6
        num_tabs_parenthetical = num_tabs_character - 1
        num_tabs_speech = 4
        tabs_character = "\t" * num_tabs_character
        tabs_speech = "\t" * num_tabs_speech
        tabs_parenthetical = "\t" * num_tabs_parenthetical
        for item in data:
            if item["type"] == "scene":
                screenplay_text += f"{item['content']}\n\n"
            elif item["type"] == "action":
                screenplay_text += f"{item['content']}\n\n"
            elif item["type"] == "dialogue":
                name = item["name"]
                modifier = item.get("modifier", "")
                parenthetical = item.get("parenthetical", "")
                speech = item["content"]
                screenplay_text += f"{tabs_character}{name} {modifier}\n"
                if parenthetical:
                    screenplay_text += f"{tabs_character}{parenthetical}\n"
                screenplay_text += f"{tabs_speech}{speech}\n\n"

        return screenplay_text

