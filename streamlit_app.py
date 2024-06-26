import streamlit as st
import win32com.client
import os

def convert_indesign_to_pdf(indd_file_path):
    app = win32com.client.Dispatch('InDesign.Application.CC.2017')
    myDocument = app.Open(indd_file_path)

    idPDFType = 1952403524
    output_files = []
    if app.Documents.Count != 0:
        directory = os.path.dirname(indd_file_path)
        docBaseName = myDocument.Name
        for x in range(0, myDocument.Pages.Count):
            myPageName = myDocument.Pages.Item(x + 1).Name
            app.PDFExportPreferences.PageRange = myPageName
            myFilePath = os.path.join(directory, f"{docBaseName[:-5]}_{myPageName}.pdf")
            myDocument.Export(idPDFType, myFilePath)
            output_files.append(myFilePath)
    myDocument.Close()
    return output_files

def main():
    st.title("InDesign to PDF Converter")
    st.write("Upload an Adobe InDesign file to convert it to PDF.")

    uploaded_file = st.file_uploader("Choose an InDesign file", type=['indd'])
    
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        indd_file_path = os.path.join("temp", uploaded_file.name)
        with open(indd_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write(f"File uploaded: {uploaded_file.name}")
        
        if st.button("Convert to PDF"):
            output_files = convert_indesign_to_pdf(indd_file_path)
            if output_files:
                st.write("Conversion successful! Download the PDF files below:")
                for pdf_file in output_files:
                    with open(pdf_file, "rb") as f:
                        st.download_button(label=f"Download {os.path.basename(pdf_file)}", data=f, file_name=os.path.basename(pdf_file), mime="application/pdf")
            else:
                st.error("Failed to convert the InDesign file to PDF.")

if __name__ == "__main__":
    if not os.path.exists("temp"):
        os.makedirs("temp")
    main()
