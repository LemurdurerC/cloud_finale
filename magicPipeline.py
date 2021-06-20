from deSkew import *
import cv2
import pytesseract
import spacy
import os




def imagePreTreatment(image):

    rotated1 = deskew1(image)
    gray = cv2.cvtColor(rotated1, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 9)

    return adaptive_threshold


def getTextFromImage(img):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)

    return text

def getEntitiesFromText(text):

    nlp = spacy.load("output/model-last")
    line = text

    total = ""
    date = ""
    company = ""
    doc = nlp(line)
    for i, ent in enumerate(doc.ents):
        print(i, "----", ent.text, ent.start_char, ent.end_char, ent.label_)
        if ent.label_ == "TOTAL":
            # print("TOTAL")
            total = ent.text
        if ent.label_ == "DATE":
            # print("DATE")
            date = ent.text
        if ent.label_ == "COMPANY":
            # print("COMPANY")
            company = ent.text

    return company, date, total

def magicPipeline(image):
    print(getEntitiesFromText(getTextFromImage(imagePreTreatment(image))))





