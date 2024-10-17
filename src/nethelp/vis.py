def get_colorblindness_colors(hex_col, colorblind_types='all'):
    """
    Generates color representations for various types of colorblindness.

    Parameters
    ----------
    hex_col (str or tuple)
        The color you wish to check, in hex code format e.g. "#ffffff" or rgb
        format e.g. (1,255,20)

    colorblind_types (str or list)
        If "all", the function returns a dictionary with all of the following:
            Protanopia - ("Dichromat" family)
                The viewer sees no red.
            Deuteranopia - ("Dichromat" family)
                The viewer sees no green.
            Tritanopia - ("Dichromat" family)
                The viewer sees no blue.
            Protanomaly - ("Anomalous Trichromat" family)
                The viewer sees low amounts of red.
            Deuteranomaly - ("Anomalous Trichromat" family).
                The viewer sees low amounts of green.
            Tritanomaly - ("Anomalous Trichromat" family).
                The viewer sees low amounts of blue.
            Achromatopsia - ("Monochromat" family)
                The viewer sees no color at all.
            Achromatomaly - ("Monochromat" family)
                The viewer sees low amounts of color.

    Returns
    -------
    colorblind_output (dict)
        dictionary where the keys are the type of colorblindness and the values
        are the re-colored version of your original hex_col. This also includes
        a grayscale version of the color.
    """
    all_vals = ['Original Color', 'Protanopia', 'Deuteranopia',
                'Protanomaly', 'Deuteranomaly',
                'Achromatopsia', 'Achromatomaly', 'Grayscale']

    if type(hex_col)!=str:
        if len(hex_col)!=3:
            print('Input a hex color please.')
            return ''
        else:
            hex_col = rgb_to_hex(hex_col)
    else:
        if "#" not in hex_col and len(hex_col)!=6:
            try:
                hex_col = namedColors[hex_col]
            except:
                print('Input a hex color please.')
                return ''

    base_url = 'https://convertingcolors.com/'
    hex_url = base_url + 'hex-color-%s.html'%hex_col.replace("#",'')
    print(hex_url)
    reqs = requests.get(hex_url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    colorblind_sec = soup.find_all('details',{'id':'blindness-simulation'})[0]
    colorblind_labels = [i.text for i in colorblind_sec.find_all('h3')]
    # colorblind_colors = np.unique([i.text for i in colorblind_sec.find_all('div')])
    tmp = np.unique([i.text for i in colorblind_sec.find_all('div')])
    colorblind_colors = [i for i in tmp for x in all_vals[1:] if x in i and all_vals[0] not in i]

    colorblind_output = {"Original Color":hex_col}

    # for i in colorblind_mappings.keys():
    #     for j in colorblind_colors:
    #         # if i in j:
    #         hex_col_j = j
    #         colorblind_output[i] = hex_col_j
    for i in colorblind_mappings.keys():
        for j in colorblind_colors:
            if i in j:
                hex_col_j = "#"+j.split('%')[-1]
                # hex_col_j = j.replace(i,'#')
                colorblind_output[i] = hex_col_j

    if colorblind_types!='all':
        if type(colorblind_types) == str:
            colorblind_types = [colorblind_types]

        new_out = {'Original Color':hex_col}
        for c in colorblind_types:
            new_out[c] = colorblind_output[c]

        colorblind_output = new_out

    colorblind_output['Grayscale'] = hex_to_grayscale(hex_col)
    for xx in all_vals:
        if xx not in list(colorblind_output.keys()):
            colorblind_output[xx] = hex_col

    return {hex_col:colorblind_output}

def rgb_to_hsv(rgb):
    """
    Converts an RGB color to HSV format.

    Parameters
    ----------
    rgb : tuple of ints
        A tuple containing the RGB values (R, G, B) where each value is in the
        range 0 to 255.

    Returns
    -------
    numpy.ndarray
        An array representing the HSV equivalent of the input RGB values.
    """
    rgb = np.array(rgb)
    rgb = rgb.astype('float')
    maxv = np.amax(rgb)
    maxc = np.argmax(rgb)
    minv = np.amin(rgb)
    minc = np.argmin(rgb)

    hsv = np.zeros(rgb.shape, dtype='float')
    hsv[maxc == minc, 0] = np.zeros(hsv[maxc == minc, 0].shape)
    hsv[maxc == 0, 0] = (((rgb[..., 1] - rgb[..., 2]) * 60.0 /\
                          (maxv - minv + np.spacing(1))) % 360.0)[maxc == 0]
    hsv[maxc == 1, 0] = (((rgb[..., 2] - rgb[..., 0]) * 60.0 /\
                          (maxv - minv + np.spacing(1))) + 120.0)[maxc == 1]
    hsv[maxc == 2, 0] = (((rgb[..., 0] - rgb[..., 1]) * 60.0 /\
                          (maxv - minv + np.spacing(1))) + 240.0)[maxc == 2]
    hsv[maxv == 0, 1] = np.zeros(hsv[maxv == 0, 1].shape)
    hsv[maxv != 0, 1] = (1 - minv / (maxv + np.spacing(1)))[maxv != 0]
    hsv[..., 2] = maxv/255

    return hsv

def lightness(hex_col):
    """
    Calculates the perceived lightness of a color.

    Parameters
    ----------
    hex_col : str
        A hex code representing the color (e.g., "#ffffff").

    Returns
    -------
    float
        The perceived lightness of the color, ranging from 0 (dark) to 1 (light).
    """    
    rgb = hex_to_rgb(hex_col)
    r,g,b = rgb
    denominator = 255 * (0.299 + 0.587 + 0.111)**(0.5)
    L = (0.299 * r**2 + 0.587 * g**2 + 0.111 * b**2)**(0.5) / denominator

    return L

def saturation(hex_col):
    """
    Calculates the saturation of a given hex color.

    Parameters
    ----------
    hex_col : str
        A hex code representing the color (e.g., "#ffffff").

    Returns
    -------
    float
        The saturation value ranging from 0 (unsaturated, grayscale) to 1 (fully saturated).
    """
    hsv = rgb_to_hsv(hex_to_rgb(hex_col))

    return hsv[1]

def hue(hex_col):
    """
    Calculates the hue of a given hex color.

    Parameters
    ----------
    hex_col : str
        A hex code representing the color (e.g., "#ffffff").

    Returns
    -------
    float
        The hue value in degrees, ranging from 0 to 360.
    """
    hsv = rgb_to_hsv(hex_to_rgb(hex_col))

    return hsv[0]

def rgb_to_hex(rgb):
    """
    Converts an RGB color to hex format.

    Parameters
    ----------
    rgb : tuple of ints
        A tuple containing the RGB values (R, G, B) where each value is in the
        range 0 to 255.

    Returns
    -------
    str
        The hex code representation of the RGB color.
    """
    r,g,b=rgb

    return '#%02x%02x%02x' % (r,g,b)

def hex_to_rgb(value):
    """
    Converts a hex color code to an RGB tuple.

    Parameters
    ----------
    value : str
        A hex code representing the color (e.g., "#ffffff").

    Returns
    -------
    tuple of ints
        A tuple containing the RGB values (R, G, B) where each value is in the range 0 to 255.
    """
    value = value.lstrip('#')
    lv = len(value)

    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

def hex_to_grayscale(hex_col):
    """
    Converts a hex color code to its grayscale equivalent.

    Parameters
    ----------
    hex_col : str
        A hex code representing the color (e.g., "#ffffff").

    Returns
    -------
    str
        The grayscale value of the color as a normalized float (0.0 to 1.0).
    """
    img = hex_to_rgb(hex_col)
    R, G, B = img
    imgGray = 0.2989 * R + 0.5870 * G + 0.1140 * B    

    return '%.7f'%(imgGray/255)