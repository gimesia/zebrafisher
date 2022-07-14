function croppedImage = getCroppedImage(binImage)

global inputImg;

[x1, y1, x2, y2] = getBBoxCoordinates(binImage);

croppedImage.bbox = [x1, y1, x2, y2];
croppedImage.mask = binImage(y1:y2, x1:x2);
croppedImage.input = inputImg(y1:y2, x1:x2);

end