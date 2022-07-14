function normalised = normaliseIntensityRange(image, rng)

d = double(image);
mx = max(max(d));
mn = min(min(d));

normalised01 = (d - mn) ./ (mx - mn);

normalised = (normalised01 * (rng.mx - rng.mn)) + rng.mn;

end