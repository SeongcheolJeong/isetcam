function optics = cos4th(oi)
%Calculate cos4th offaxis fall off data
%
% Synopsis
%   optics = cos4th(oi)
%
% Description
%  The irradiance of a uniform radiance input field declines as we move
%  from the principal axis to off-axis locations.  This is called the
%  relative illumination, or sometimes the cos4th fall off.  The cos4th
%  formula is a good approximation in many cases.  More detailed
%  calculations for specific lenses can be obtained using ray trace
%  methods.
%
%  The algorithm in this routine handles the case of a distant image
%  separately from that of a close image.
%
% Formula:
%   d  = distance from the lens to the image plane
%   s  = sqrt(d^2 + fieldHeight^2)
%   fN = f-number
%
% If d > 10*image diagonal size
%   RI = (d / sFactor).^4;
% else
%   m = magnification
%   {A complicated formula}
%
% Example:
%
% Copyright ImagEval Consultants, LLC, 2003.

%% Setting up local variables
optics = oiGet(oi,'optics');

sSupport = oiGet(oi,'spatialsupport');
x = sSupport(:,:,2);
y = sSupport(:,:,1);

imageDistance = opticsGet(optics,'imagedistance');
imageDiagonal = oiGet(oi,'diagonal');

fNumber = opticsGet(optics,'fNumber');
sFactor = sqrt(imageDistance.^2 + (x.^2 + y.^2));

%% Calculate the spatial fall off from the center of the lens
if (imageDistance > 10*imageDiagonal)
    % Use if imageDistance >> imageDiagonal
    spatialFall = (imageDistance./sFactor).^4;
else
    % Use if imageDistance ~ imageDiagonal. This code was created by PC.
    % It has that 1 + for the radiance to irradiance conversion.
    %
    % Notice that this formula depends on the fnumber, but only for a scale
    % factor.
    %
    % This expression agrees with the other cos4th expression when
    % imageDistance >> imageDiagonal
    magnification =  opticsGet(optics,'magnification');

    % If imageDistance >> max(sFactor) cos_phi = 1 and sin_phi = 0
    %
    cos_phi = (imageDistance ./ sFactor);  %figure(3); mesh(cos_phi)
    sin_phi = sqrt(1-cos_phi.^2);          %figure(3); mesh(sin_phi)
    tan_phi = sin_phi ./ cos_phi;          %figure(3); mesh(tan_phi)
    
    % Here is the fnumber
    sin_theta = 1 ./ (1 + 4*(fNumber*(1-magnification))^2);
    cos_theta = sqrt(1 - sin_theta.^2);
    tan_theta = sin_theta ./ cos_theta;
    
    % This really needs a comment
    spatialFall = ( pi / 2) * (1 - (1 - tan_theta.^2 + tan_phi.^2) ...
        ./ sqrt(tan_phi.^4 + 2*tan_phi.^2*(1-tan_theta.^2)+1./cos_theta.^4));
    spatialFall = spatialFall./(pi*sin_theta.^2);
end

%% figure; mesh(spatialFall)
optics = opticsSet(optics,'cos4th data',spatialFall);

end
