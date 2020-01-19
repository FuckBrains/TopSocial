from PIL import Image, ImageDraw


def watermarkimage(file_name, watermark_filepath):
    # Open the original image
    main = Image.open(file_name)

    # Create a new image for the watermark with an alpha layer (RGBA)
    #  the same size as the original image
    # watermark = Image.new("RGBA", main.size)
    # Get an ImageDraw object so we can draw on the image
    # waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
    # Place the text at (10, 10) in the upper left corner. Text will be white.
    # waterdraw.text((watermark_width, watermark_height), watermark_text)
    watermark = Image.open(watermark_filepath)

    # Get the watermark image as grayscale and fade the image
    # See <http://www.pythonware.com/library/pil/handbook/image.htm#Image.point>
    #  for information on the point() function
    # Note that the second parameter we give to the min function determines
    #  how faded the image will be. That number is in the range [0, 256],
    #  where 0 is black and 256 is white. A good value for fading our white
    #  text is in the range [100, 200].

    desiredwatermart_width = int(main.width / 4)
    desiredwatermart_height = int((watermark.height / watermark.width) * desiredwatermart_width)

    left = int((main.width / 2) - (desiredwatermart_width/2))
    top = int((main.height / 2) - (desiredwatermart_height / 2))


    watermark_image = watermark.resize((desiredwatermart_width, desiredwatermart_height))
    watermask_image = watermark_image.convert("L").point(lambda x: min(x, 300))
    # Apply this mask to the watermark image, using the alpha filter to
    #  make it transparent
    watermark_image.putalpha(watermask_image)



    # Paste the watermark (with alpha layer) onto the original image and save it
    main.paste(watermark_image, (left,top), watermask_image)
    main.save(file_name, "JPEG")


# if __name__ == '__main__':
#     watermarkimage("../../cdn/content/insta/BR0Vcl4gAF5/thumbnail_BR0Vcl4gAF5.jpg", "../../cdn/Image/play.png")
