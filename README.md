mecharat
========

Robot Assisted Transcriptions

# Problem
We now have decent, open source tools to exract typewritten text and tabular data from PDFs thanks to tools like [Tesseract](https://code.google.com/p/tesseract-ocr/) and [Tabula](https://github.com/tabulapdf/tabula-extractor).

However, form data is still very hard, particularly when the form response is hand written. Within our community, this is still typically done by hand. That means it's often not done at all.

# Prior Art
For the 2012 Election, Propublica created an site, [Free the Files](https://projects.propublica.org/free-the-files/), for their readers to help them track "dark money" by transcribing payers for political advertising from televisions station invoices. 

The heart of the site was a tool called [transcribable](https://github.com/propublica/transcribable). After logging in,
 a user would ask for a invoice to transcribe, an invoice would be fetched from [DocumentCloud](http://www.documentcloud.org/home), the user would extract four pieces of information from the invoice, submit the information, and another task would be automatically loaded.
 
Transcribable included a number of features that made it [very easy to start transcribing, keep transcribing, and make transcribing compelling](http://www.propublica.org/nerds/item/casino-driven-design).

However, even with these strong design elements and this unusally compelling purpose of tracking dark money, the vast majority of invoices were not transcribed.

# Mechanical Extensions
Using computer vision, the amount of necessary labor for form transcription can be dramatically reduced.

1. Reduced task switching. Forms and invoices of the same type look very similar. We should be able to cluster and present similar looking documents to the user to transcribe. The user will already know where to look in the document for the necessary information.
2. Reverse Templates. If the same information appears in the same place for every form of a certain type, we should be able focus on just that area. Instead of presenting the entire form to the user to scan through, we can just present her the relevant areas to transcribe.
3. Confirming Extraction. If we understand the template for a document, we may be able to extract the relevant document using OCR. Transcribing could start with our best, OCR, attempt to fill in the information. The user either accepts or corrects the information.
4. Recognizing handwritten information. If we understand the template for a document, when a user transcribes handwritten information we can store, as an image, the relevant part of the document. Although we may not be able to OCR handwritten information, we can try to match a new form field image against a growing set of identified images.

# Other use cases
1. In Illnois, political workers collection petitions to get on the ballot have to sign their names at the bottom of the petition forms. Information on who is working on what campaigns can provide very useful information about political alliances. Using these forms, Dan Mihapoulos was able to find that Alderman Ed Burke was sending his political workers to support Gery Chico in the 2011 Chicago mayoral race, even though Burke said he was neutral.
2. Zoning Reclassification Applications include information on the person making the application and what they want to do with land. Timely access to this information is of interest to neighbors and local community groups.







