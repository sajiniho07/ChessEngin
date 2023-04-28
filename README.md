# Chess Board Detection and Prediction in Problem_4 solution

## About

This project is focused on detecting the current state of a chess board from an image and predicting the move made between two images.

This problem was requested by this website in the form of a programming contest: https://roboepics.com/c/DueMLBlitz/overview

## Installation

This project requires Python 3.6 or later version, along with the following libraries:

- numpy
- pandas
- opencv-python
- scikit-image
- python-chess

## Usage

To use this project, simply run the main.py file after downloading the source code. You can modify the image paths in the main.py file to process your own images.

The count_files_with_extension() function is used to count the number of files with a specific extension in a directory. The medianBlur() function is used to smoothen an image. The sharp_image() function is used to sharpen an image. The crop_image_border() function is used to crop the border of an image. The populate_board() function is used to populate the state of a chess board given an image and a mask. The get_piece_type() function is used to determine the type of a piece given its filename. The get_fen_from_board() function is used to extract the FEN string representation of the current state of a chess board given an image. Finally, the get_move() function is used to predict the move made between two states of a chess board.

In this implementation, the main.py file processes a set of 'before' and 'after' chessboard images, extracts the current FEN state for each image, predicts the move made between the two states, and writes the results to a CSV file named predictions.csv.

## License ##

Made with :heart: by <a href="https://github.com/sajiniho07" target="_blank">Sajad Kamali</a>

<a href="#top">Back to top</a>
