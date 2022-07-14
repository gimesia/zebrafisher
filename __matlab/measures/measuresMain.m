

function measureProps = measuresMain(fishProps)

fishImg = fishProps.filledFish;
eyeProperties = fishProps.eyePosCent;
eyeImg = fishProps.eyePosCent.eyeImg;
head = fishProps.head;

fishEyeProps = getFishEyes(eyeImg, fishProps, eyeProperties);

fullBodySkelProps = getFullBodyLength(fishImg, fishProps, eyeProperties);

endPointsProps = ...
    getDistanceBetween2EndPoints(fullBodySkelProps, fishProps.segmentedOrigSizeFish, head, fishProps);

% getYolkSacDiameter(fishProps, eyeProperties, fullBodySkelProps, endPointsProps);

measureProps.body = fullBodySkelProps;
measureProps.bodyImg = fullBodySkelProps.origSizeSkeleton;
measureProps.eyeProps = fishEyeProps;
measureProps.endXY = endPointsProps.points;

measures.eyeDiam = fishEyeProps.eyeDiam;
measures.endPointsDist = endPointsProps.endDist;
measureProps.measures = measures;

end
