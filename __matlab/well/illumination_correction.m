function output_image = illumination_correction(input_image)

display_scale = 2;

%figure; imshow(input_image(1:display_scale:end,1:display_scale:end)); title('Input');
%figure; imshow(input_image); title('Original');

% min_input=min(min(GRAY))
% max_input=max(max(GRAY))
% mean_input=mean2(GRAY)
% std_input=std2(GRAY)
 
corr = local_contrast_enhancement(input_image);

% min_ce=min(min(corr))
% max_ce=max(max(corr))
% mean_ce=mean2(corr)
% std_ce=std2(corr)

corr_mask = get_mask_for_correction(corr);

% min_mask=min(min(corr_mask))
% max_mask=max(max(corr_mask))
% mean_mask=mean2(corr_mask)
% std_mask=std2(corr_mask)

RESULT = robust_homomorphic_surface_fitting(input_image, corr_mask);

% min_result=min(min(corrd2))
% max_result=max(max(corrd2))
% mean_result=mean2(corrd2)
% std_result=std2(corrd2)
% figure; imshow(GRAY);
% figure; imshow(mat2gray(corrd2));
 

%figure; imshow(RESULT(1:display_scale:end,1:display_scale:end)); title('Result');
% min(min(GRAY))
% max(max(GRAY))
% mean2(GRAY)
% std2(GRAY)
% sum(sum(double(GRAY).*double(~MaskFOV)))/sum(sum(~MaskFOV))

output_image = RESULT;

