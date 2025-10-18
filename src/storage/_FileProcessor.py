import fitz
import os
import pandas as pd
import re
import docx
import pytesseract
from PIL import Image
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.document import Document


class FileProcessor:
	def __init__(self):
		pass
	
	def process_file(self, file_path, mongo_db=None):
		if not os.path.exists(file_path):
			return(f"Error: File not found at path {file_path}")

		result = None
		_, file_extension = os.path.splitext(file_path)
		file_extension = file_extension.lower()

		if file_extension in ['.xlsx', '.xls']:
			result = self.process_excel_document(file_path)
		elif file_extension.lower() == '.pdf':
			result = self.process_pdf_document(file_path)
		elif file_extension in ['.docx', '.doc']:
			result = self.process_word_document(file_path)
		elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
			result = self.process_images(file_path)
		elif file_extension == '.csv':
			result = self.process_csv_document(file_path)
		else:
			return f"Error: Unsupported file type '{file_extension}'"
		if mongo_db:
			mongo_db.insert_doc(result.copy())
		return result

	@staticmethod
	def clean_text(raw_text):
		text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
		text = re.sub(r'\s+', ' ', text)
		return text

	def ocr_image(self, image):
		try:
			return pytesseract.image_to_string(image)
		except Exception as e:
			return(f"Pytesseract OCR failed: {e}")


	def process_pdf_document(self, file_path):
		try:
			doc = fitz.open(file_path)
			pdf_data = {
				"metadata": {
					"source": os.path.basename(file_path),
					"type": "pdf",
					"num_pages": len(doc)
				},
				"pages": []
			}

			for page_num, page in enumerate(doc):
				page_content = {
					"page_number": page_num + 1,
					"content": "",
					"ocr_attempted": False
				}
				
				page_text = page.get_text()

				if len(page_text.strip()) < 100:
					page_content["ocr_attempted"] = True
					pix = page.get_pixmap(dpi=300)
					img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
					ocr_text = self.ocr_image(img)
					if len(ocr_text) > len(page_text):
						page_content["content"] = self.clean_text(ocr_text)
					else:
						page_content["content"] = self.clean_text(page_text)
				else:
					page_content["content"] = self.clean_text(page_text)
				
				pdf_data["pages"].append(page_content)

			doc.close()
			return pdf_data

		except Exception as e:
			return {"error": f"An error occurred during PDF processing: {e}"}

	def process_excel_document(self, file_path):
		try:
			result = {
				"metadata": {
					"source": os.path.basename(file_path),
					"type": "excel"
				},
				"content": {}
			}
			xls = pd.ExcelFile(file_path)
			all_sheets_data = {}
			for sheet_name in xls.sheet_names:
				df = pd.read_excel(xls, sheet_name=sheet_name)

				if df.empty:
					continue

				df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r'[^a-zA-Z0-9_]', '', regex=True)
				
				sheet_data = df.to_dict(orient='records')
				all_sheets_data[sheet_name] = sheet_data
			
			result["content"] = all_sheets_data
			return result

		except Exception as e:
			return f"Error processing Excel file: {e}"

	def process_csv_document(self, file_path):
		try:
			df = pd.read_csv(file_path)
			df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r'[^a-zA-Z0-9_]', '', regex=True)
			json_file = {
				"metadata": {
					"source": os.path.basename(file_path),
					"type": "csv"
				},
				
				"content": df.to_dict(orient='records')
			}
			return json_file

		except Exception as e:
			return (f"Error processing CSV file: {e}")

	@staticmethod
	def iter_block_items(parent):
		if isinstance(parent, Document):
			parent_elm = parent.element.body
		else:
			raise ValueError("Parent must be a Document object")

		for child_elm in parent_elm.iterchildren():
			if child_elm.tag.endswith('p'):
				yield Paragraph(child_elm, parent)
			elif child_elm.tag.endswith('tbl'):
				yield Table(child_elm, parent)

	def process_word_document(self, file_path):
		try:
			doc = docx.Document(file_path)
			doc_data = {
				"metadata": {
					"source": os.path.basename(file_path),
					"type": "word",
				},
				"content": []
			}

			for block in self.iter_block_items(doc):
				if isinstance(block, Paragraph):
					text = block.text.strip()
					if text:
						doc_data["content"].append({
							"type": "paragraph",
							"text": text
						})
				elif isinstance(block, Table):
					table_data = []
					for row in block.rows:
						row_data = [cell.text.strip() for cell in row.cells]
						table_data.append(row_data)
					if table_data:
						doc_data["content"].append({
							"type": "table",
							"rows": table_data
						})
			
			return doc_data

		except Exception as e:
			return {"error": f"Error processing Word file: {e}"}

	def process_images(self, file_path):
		image_data = {
				"metadata": {
					"source": os.path.basename(file_path),
					"type": "image"
				},
				"content": ''
			}
		image_content = self.ocr_image(Image.open(file_path))
		image_data["content"] = image_content
		return image_data