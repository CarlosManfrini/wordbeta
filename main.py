from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from reportlab.pdfgen import canvas
from kivy.uix.label import Label
import os


class WordLikeApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # Toolbar for text styles and actions
        self.toolbar = BoxLayout(size_hint_y=0.1)
        self.add_widget(self.toolbar)

        # Font Style Spinner
        self.font_spinner = Spinner(
            text="Font",
            values=["Helvetica", "Courier", "Times-Roman"],
            size_hint=(0.2, 1),
        )
        self.font_spinner.bind(text=self.change_font)
        self.toolbar.add_widget(self.font_spinner)

        # Font Size Spinner
        self.size_spinner = Spinner(
            text="12",
            values=["10", "12", "14", "18", "24", "32"],
            size_hint=(0.2, 1),
        )
        self.size_spinner.bind(text=self.change_font_size)
        self.toolbar.add_widget(self.size_spinner)

        # Insert Image Button
        self.image_button = Button(text="Insert Image", size_hint=(0.2, 1))
        self.image_button.bind(on_release=self.open_file_chooser)
        self.toolbar.add_widget(self.image_button)

        # Save Button (PDF)
        self.save_button = Button(text="Save as PDF", size_hint=(0.2, 1))
        self.save_button.bind(on_release=self.save_as_pdf)
        self.toolbar.add_widget(self.save_button)

        # Main Text Area
        self.text_input = TextInput(
            font_size=14, multiline=True, size_hint=(1, 0.8), text=""
        )
        self.add_widget(self.text_input)

        # Image Area
        self.image_area = BoxLayout(size_hint=(1, 0.4))
        self.add_widget(self.image_area)

        self.current_image_path = None

    def change_font(self, spinner, text):
        """Change the font style."""
        self.text_input.font_name = text

    def change_font_size(self, spinner, text):
        """Change the font size."""
        self.text_input.font_size = int(text)

    def open_file_chooser(self, instance):
        """Open file chooser to insert an image."""
        content = FileChooserListView()
        popup = Popup(title="Select an Image", content=content, size_hint=(0.9, 0.9))

        def load_image(*args):
            selected = content.selection
            if selected:
                self.insert_image(selected[0])
                popup.dismiss()

        content.bind(on_submit=load_image)
        popup.open()

    def insert_image(self, filepath):
        """Insert an image into the editor."""
        if self.image_area.children:
            self.image_area.clear_widgets()
        self.current_image_path = filepath
        image_widget = Image(source=filepath, allow_stretch=True)
        self.image_area.add_widget(image_widget)

    def save_as_pdf(self, instance):
        """Save the document as a PDF."""
        save_popup = Popup(title="Saving as PDF...", size_hint=(0.8, 0.4))

        def save_to_pdf(instance):
            # Save the text content
            pdf_path = "document.pdf"
            pdf = canvas.Canvas(pdf_path)
            pdf.setFont(self.font_spinner.text, int(self.size_spinner.text))

            # Write the text
            lines = self.text_input.text.split("\n")
            y_position = 800
            for line in lines:
                pdf.drawString(50, y_position, line)
                y_position -= 20

            # Insert the image if available
            if self.current_image_path:
                pdf.drawImage(self.current_image_path, 50, y_position - 200, width=300, height=200)

            pdf.save()
            save_popup.dismiss()
            success_popup = Popup(
                title="Success!",
                content=Label(text=f"PDF saved at {os.path.abspath(pdf_path)}"),
                size_hint=(0.8, 0.4),
            )
            success_popup.open()

        # Display a save popup
        save_button = Button(text="Save", size_hint=(0.4, 0.4))
        save_button.bind(on_release=save_to_pdf)
        save_popup.content = save_button
        save_popup.open()


class WordApp(App):
    def build(self):
        return WordLikeApp()


if __name__ == "__main__":
    WordApp().run()
