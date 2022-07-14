%% (iterative) robust homomorphic surface fitting

function output = robust_homomorphic_surface_fitting(input, mask)
%

%fprintf('robust homomorphic surface fitting\n');

gd = input;
gd(mask) = 0;
%figure; imshow(gd);

sub = 4;

%size(input)

Fo = double(input);
FLo = log(1+Fo);
FLov = FLo(:);

F = Fo(1:sub:end,1:sub:end);
%figure; imshow(mat2gray(F)); title('Subsampled Input');

FL = log(1+F);
FLv = FL(:);

NM = size(FLv,1);
NN = size(FL,1);
MM = size(FL,2);

deg = 4;
S = zeros(NM,2^deg-1);
for yi = 0:MM-1,
    for xi = 0:NN-1,
        sp = 0;
        for pp = deg:-1:0,
            for xp = pp:-1:0,
                yp = pp-xp;
                S(yi*NN+xi+1,sp+1) = xi^xp*yi^yp;
                sp = sp+1;
            end
        end
    end
end

Wc = ones(NM,1);
masksub = mask(1:sub:end,1:sub:end);
Wc(masksub(:)) = 0;
W = spdiags(Wc,0,NM,NM);

Y = W*S;

%pinv does not work when compiled with mcc
%because it uses 'svd' which does not work
%P = my_pinv(Y);
%P = pinv(Y);
%{
P=inv(Y'*Y)*Y';

P = P*FLv;
%}
P = Y\FLv;

SP = S*P;
ILv = exp(SP);
RLv = exp(FLv-SP);
IL = reshape(ILv, size(FL));
RL = reshape(RLv, size(FL));

%figure; imshow(mat2gray(F)); title('F');
%figure; imshow(mat2gray(FL)); title('FL');
%figure; imshow(mat2gray(IL)); title('IL');
%figure; imshow(mat2gray(RL)); title('RL');

SPo2 = zeros(sub*size(FL));
for xi = 1:sub,
    for yi = 1:sub,
        SPo2(xi:sub:end,yi:sub:end) = reshape(SP, size(FL));
    end
end
%figure; imshow(mat2gray(SPo2)); title('SPo2');

SPo = SPo2(1:size(FLo,1),1:size(FLo,2));
%figure; imshow(mat2gray(SPo(1:2:end,1:2:end))); title('SPo');

SPs = imfilter(SPo, fspecial('gaussian', 3, 1));
%figure; imshow(mat2gray(SPs)); title('SPs');

SPov = SPs(:);
%figure; imshow(mat2gray(SPov)); title('SPov');

ILov = exp(SPov);
%figure; imshow(mat2gray(ILov)); title('ILov');

RLov = exp(FLov-SPov);
%figure; imshow(mat2gray(RLov)); title('RLov');

osize = size(FLo);

ILo = reshape(ILov, osize);
%figure; imshow(mat2gray(ILo)); title('ILo');

RLo = reshape(RLov, size(FLo));
%figure; imshow(mat2gray(RLo)); title('RLo');

GRAYd = RLo/2;
output = uint8(GRAYd*255);
