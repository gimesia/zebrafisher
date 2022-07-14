function P = my_pinv(A)

%fprintf('my pseudoinverse\n');
%[U, Sigma, V] = svd(A,0);
[U, Sigma, V] = svds(A,16);
 Sigma= Sigma';
 s = size(Sigma);
 Sigma = full(spdiags( 1./diag( Sigma ), 0, s(1), s(2)) );
 P = (V*Sigma)*U';
 
 %sum(sum(P-pinv(A)))  %only for evaluation
