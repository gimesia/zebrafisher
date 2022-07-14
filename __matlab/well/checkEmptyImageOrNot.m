
function objectInImg = checkEmptyImageOrNot(image)

[row, col] = find(image);

if isempty(row) || isempty(col)
    objectInImg = 'false';
else
    objectInImg = 'true';
end

end