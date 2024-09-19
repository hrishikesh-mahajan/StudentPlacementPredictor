# Description: This file contains functions to set the page dimensions of a word document.
from docx.shared import Inches


def set_page_dim(document, left,right,top,bottom,height):
    """
    Set the page width of a document.
    """
    sections = document.sections
    for section in sections:
        section.left_margin = Inches(left)  # Adjust left margin if needed
        section.right_margin = Inches(right)  # Adjust right margin if needed
        section.top_margin = Inches(top)  # Adjust top margin if needed
        section.bottom_margin = Inches(bottom)  # Adjust bottom margin if needed
        section.page_height = Inches(height)  # Adjust height if needed

def set_page_height(document, height):
    """
    Set the page height of a document.
    """
    sections = document.sections
    for section in sections:
        section.page_height = Inches(height)

def set_page_width(document, width):
    """
    Set the page width of a document.
    """
    sections = document.sections
    for section in sections:
        section.page_width = Inches(width)

def set_page_left_margin(document, left_margin):
    """
    Set the page left margin of a document.
    """
    sections = document.sections
    for section in sections:
        section.left_margin = Inches(left_margin)

def set_page_right_margin(document, right_margin):
    """
    Set the page right margin of a document.
    """
    sections = document.sections
    for section in sections:
        section.right_margin = Inches(right_margin)

def set_page_top_margin(document, top_margin):
    """
    Set the page top margin of a document.
    """
    sections = document.sections
    for section in sections:
        section.top_margin = Inches(top_margin)

def set_page_bottom_margin(document, bottom_margin):
    """
    Set the page bottom margin of a document.
    """
    sections = document.sections
    for section in sections:
        section.top_margin = Inches(bottom_margin)
