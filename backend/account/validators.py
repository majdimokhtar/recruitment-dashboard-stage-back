import os



def validate_file_extension(name):
    isValid = True
    
    
    ext = os.path.splitext(name)[1] # ("name of the pdf" , ".pdf")
    valide_extenstion = [".pdf"]
    
    if not ext.lower() in valide_extenstion:
        isValid =False
        
    return isValid