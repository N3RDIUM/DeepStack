import sep

def extract_background(imdata, bw, bh, fw, fh):
    """
    Extracts the background from an image
    """
    background = sep.Background(imdata, bw=bw, bh=bh, fw=fw, fh=fh)
    bkg = background.back()
    return bkg

def remove_background(imdata, bw, bh, fw, fh):
    """
    Removes the background from an image
    """
    bkg = extract_background(imdata, bw, bh, fw, fh)
    data_sub = imdata - bkg
    return data_sub