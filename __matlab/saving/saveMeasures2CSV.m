

function saveMeasures2CSV(measures, filename, csoport, kor, sfilename)

header = {'kép kód', 'forrás', 'csoport', 'kor', '2 végpont(pixel)', ...
    'yolk sac nagysága(pixel)', 'szem nagysága(pixel)', 'validitás', ...
    'megjegyzés', 'wellTime', 'fishTime', 'measTime'};

for m = 1 : size(measures, 2)
    meas = measures{m};
    data = zeros(size(header));
    
    dataS = meas(3);

    data(3) = csoport;
    data(4) = kor;
    data(5) = meas{2};
    data(7) = meas{1};
    data(10) = meas{4};
    data(11) = meas{5};
    data(12) = meas{6};
    
    allData(m, :) = data;
    stringData(m, :) = dataS;
end

% fname = sprintf('%s/images.txt', sfilename);
% filePh = fopen(fname,'w');
% fprintf(filePh, '%s\n', stringData{:});
% fclose(filePh);

csvwriteh(filename, allData, header);

end

function csvwriteh( filename, data, header )

if exist( 'filename', 'var' )
    if ~ischar( filename )
        error('filename not char')
    end
else
    error('filename does not exists')
end
% data parameter
if exist( 'data', 'var' )
    if ~isnumeric( data )
        error('data not numeric')
    end
else
    error('data does not exist')
end
% header parameter
if exist( 'header', 'var' )
    if ~iscellstr( header )
        error('header no cell str')
    end
else
    error('header does not exist')
end

% check dimensions of data and header
[~, dcol] = size (data);
[~, hcol] = size (header);
if hcol ~= dcol
    error( 'header not of same length as data (columns)' )
end

% open file
outid = fopen (filename, 'w+');

% write header
for idx = 1:hcol
    fprintf (outid, '%s', header{idx});
    if idx ~= hcol
        fprintf (outid, ';');
    else
        fprintf (outid, '\n' );
    end
end
% close file
fclose(outid);

% write data
dlmwrite (filename, data, '-append', 'delimiter', ';');

end