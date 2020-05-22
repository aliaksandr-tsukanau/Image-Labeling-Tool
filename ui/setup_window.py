from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QRadioButton, QFileDialog, QDesktopWidget

from ui.labeler_window import LabelerWindow


class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window variables
        self.width = 800
        self.height = 940

        # State variables
        self.selected_folder = ''
        self.selected_labels = ''
        self.num_labels = 0
        self.label_inputs = []
        self.label_headlines = []
        self.mode = 'csv'  # default option

        # Labels
        self.headline_folder = QLabel('1. Select folder containing images you want to label', self)
        self.headline_num_labels = QLabel('3. Specify labels', self)
        self.labels_file_description = QLabel(
            'a) select file with labels (text file containing one label on each line)', self)
        self.labels_inputs_description = QLabel('b) or specify how many unique labels you want to assign', self)

        # self.headline_num_labels = QLabel('3. How many unique labels do you want to assign?', self)

        self.headline_label_inputs = QLabel(self)  # don't show yet
        self.selected_folder_label = QLabel(self)
        self.error_message = QLabel(self)

        # Buttons
        self.browse_button = QtWidgets.QPushButton("Browse", self)
        self.confirm_num_labels = QtWidgets.QPushButton("Ok", self)
        self.next_button = QtWidgets.QPushButton("Next", self)
        self.browse_labels_button = QtWidgets.QPushButton("Select labels", self)

        # Inputs
        self.numLabelsInput = QLineEdit(self)

        # Validation
        self.onlyInt = QIntValidator()

        # Init
        self.init_ui()

    def init_ui(self):
        # self.selectFolderDialog = QFileDialog.getExistingDirectory(self, 'Select directory')
        self.setWindowTitle('PyQt5 - Annotation tool - Parameters setup')
        self.setGeometry(0, 0, self.width, self.height)
        self.centerOnScreen()

        self.headline_folder.setGeometry(60, 30, 500, 20)
        self.headline_folder.setObjectName("headline")

        self.selected_folder_label.setGeometry(60, 60, 550, 26)
        self.selected_folder_label.setObjectName("selectedFolderLabel")

        self.browse_button.setGeometry(611, 59, 80, 28)
        self.browse_button.clicked.connect(self.pick_new)

        # Input number of labels
        top_margin_num_labels = 260
        self.headline_num_labels.move(60, top_margin_num_labels)
        self.headline_num_labels.setObjectName("headline")

        self.labels_file_description.move(60, top_margin_num_labels + 30)
        # self.browse_labels_button.setGeometry(60, top_margin_num_labels + 60, 80, 28)
        self.browse_labels_button.setGeometry(460, top_margin_num_labels + 25, 89, 28)

        self.browse_labels_button.clicked.connect(self.pick_labels_file)

        # self.labels_inputs_description.move(60, top_margin_num_labels + 100)
        self.labels_inputs_description.move(60, top_margin_num_labels + 60)
        # self.numLabelsInput.setGeometry(60, top_margin_num_labels + 130, 60, 26)
        self.numLabelsInput.setGeometry(75, top_margin_num_labels + 90, 60, 26)

        self.numLabelsInput.setValidator(self.onlyInt)
        self.confirm_num_labels.setGeometry(136, top_margin_num_labels + 89, 80, 28)
        self.confirm_num_labels.clicked.connect(self.generate_label_inputs)

        # Next Button
        self.next_button.move(360, 880)
        self.next_button.clicked.connect(self.continue_app)
        self.next_button.setObjectName("blueButton")

        # Erro message
        self.error_message.setGeometry(20, 810, self.width - 20, 20)
        self.error_message.setAlignment(Qt.AlignCenter)
        self.error_message.setStyleSheet('color: red; font-weight: bold')

        self.init_radio_buttons()

        # apply custom styles
        try:
            styles_path = "./styles.qss"
            with open(styles_path, "r") as fh:
                self.setStyleSheet(fh.read())
        except:
            print("Can't load custom stylesheet.")

    def init_radio_buttons(self):
        """
        Creates section with mode selection
        """

        top_margin = 115
        radio_label = QLabel('2. Select mode', self)
        radio_label.setObjectName("headline")
        radio_label.move(60, top_margin)

        radiobutton = QRadioButton(
            "csv (Images in selected folder are labeled and then csv file with assigned labels is generated.)", self)
        radiobutton.setChecked(True)
        radiobutton.mode = "csv"
        radiobutton.toggled.connect(self.mode_changed)
        radiobutton.move(60, top_margin + 35)

        radiobutton = QRadioButton(
            "copy (Creates folder for each label. Labeled images are copied to these folders. Csv is also generated)",
            self)
        radiobutton.mode = "copy"
        radiobutton.toggled.connect(self.mode_changed)
        radiobutton.move(60, top_margin + 65)

        radiobutton = QRadioButton(
            "move (Creates folder for each label. Labeled images are moved to these folders. Csv is also generated)",
            self)
        radiobutton.mode = "move"
        radiobutton.toggled.connect(self.mode_changed)
        radiobutton.move(60, top_margin + 95)

    def mode_changed(self):
        """
        Sets new mode (one of: csv, copy, move)
        """
        radioButton = self.sender()
        if radioButton.isChecked():
            self.mode = radioButton.mode

    def pick_new(self):
        """
        shows a dialog to choose folder with images to label
        """
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")

        self.selected_folder_label.setText(folder_path)
        self.selected_folder = folder_path

    def pick_labels_file(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select labels", "",
                                                  "Text files (*.txt)", options=options)
        if fileName:
            with open(fileName) as f:
                content = f.readlines()

            labels = [line.rstrip('\n') for line in content]

            print(labels)
            self.numLabelsInput.setText(str(len(labels)))
            self.generate_label_inputs()

            # fill the input fileds with loaded labels
            for input, label in zip(self.label_inputs, labels):
                input.setText(label)

    def generate_label_inputs(self):
        """
        Generates input fields for labels. The layout depends on the number of labels.
        """

        # check that number of labels is not empty
        if self.numLabelsInput.text().strip() != '':

            # convert string (number of labels) to integer
            self.num_labels = int(self.numLabelsInput.text())

            # delete previously generated widgets
            for input, headline in zip(self.label_inputs, self.label_headlines):
                input.deleteLater()
                headline.deleteLater()

            # initialize values
            self.label_inputs = []
            self.label_headlines = []  # labels to label input fields

            # show headline for this step
            margin_top = 400
            self.headline_label_inputs.setText('4. Fill in the labels and click "Next"')
            self.headline_label_inputs.setGeometry(60, margin_top, 300, 20)
            self.headline_label_inputs.setStyleSheet('font-weight: bold')

            # diplsay input fields
            x_shift = 0  # variable that helps to compute x-coordinate of label in UI
            for i in range(self.num_labels):
                # append widgets to lists
                self.label_inputs.append(QtWidgets.QLineEdit(self))
                self.label_headlines.append(QLabel(f'label {i + 1}:', self))

                # select particular widget
                label_input = self.label_inputs[i]
                label = self.label_headlines[i]

                # place widget in GUI (create multiple columns if there is more than 10 button)
                y_shift = (30 + 10) * (i % 10)
                if i != 0 and i % 10 == 0:
                    x_shift += 240
                    y_shift = 0

                # place input and labels in GUI
                label_input.setGeometry(60 + 60 + x_shift, y_shift + margin_top + 45, 120, 26)
                label.setGeometry(60 + x_shift, y_shift + margin_top + 45, 60, 26)

                # show widgets
                label_input.show()
                label.show()

    def centerOnScreen(self):
        """
        Centers the window on the screen.
        """
        resolution = QDesktopWidget().screenGeometry()
        self.move(int((resolution.width() / 2) - (self.width / 2)),
                  int((resolution.height() / 2) - (self.height / 2)) - 40)

    def check_validity(self):
        """
        :return: if all the necessary information is provided for proper run of application. And error message
        """
        if self.selected_folder == '':
            return False, 'Input folder has to be selected (step 1)'

        num_labels_input = self.numLabelsInput.text().strip()
        if num_labels_input == '' or num_labels_input == '0':
            return False, 'Number of labels has to be number greater than 0 (step 3).'

        if len(self.label_inputs) == 0:
            return False, "You didn't provide any labels. Select number of labels and press \"Ok\""

        for label in self.label_inputs:
            if label.text().strip() == '':
                return False, 'All label fields has to be filled (step 4).'

        return True, 'Form ok'

    def continue_app(self):
        """
        If the setup form is valid, the LabelerWindow is opened and all necessary information is passed to it
        """
        form_is_valid, message = self.check_validity()

        if form_is_valid:
            label_values = []
            for label in self.label_inputs:
                label_values.append(label.text().strip())

            self.close()
            # show window in full-screen mode (window is maximized)
            LabelerWindow(label_values, self.selected_folder, self.mode).showMaximized()
        else:
            self.error_message.setText(message)