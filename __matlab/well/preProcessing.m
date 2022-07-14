function filteredImg = preProcessing(image)

se = strel('disk', 15, 8);
imageClosed = imclose(image, se);

filteredImg = illumination_correction(imageClosed);

filteredImg = fibermetric(filteredImg, 113, 'ObjectPolarity', 'dark');

end
