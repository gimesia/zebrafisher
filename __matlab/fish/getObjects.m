
function thisobj = getObjects(label, ccimg)

tempObject = ismember(ccimg, label);
[r, c] = find(tempObject > 0);

thisobj.row = r;
thisobj.col = c;
thisobj.cc = tempObject;

end