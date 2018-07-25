#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/calib3d/calib3d.hpp"
#include "opencv2/highgui/highgui.hpp"

#include <iostream>
#include <string>

std::vector<cv::Point2d> Generate2DPoints();
std::vector<cv::Point3d> Generate3DPoints();

int main( int argc, char* argv[])
{
  // Read points
  std::vector<cv::Point2d> imagePoints = Generate2DPoints();
  std::vector<cv::Point3d> objectPoints = Generate3DPoints();

  // This is the Known Projection Matrix from Projection.matrices.hpp (its a 3 by 4 matrix)
  
  cv::Mat P(3,4,cv::DataType<float>::type);
  P.at<float>(0,0) = 2.91694788e+01;
  P.at<float>(1,0) = -2.14379115e+03;
  P.at<float>(2,0) = 1.24834322e-02;

  P.at<float>(0,1) = -9.97213328e+02;
  P.at<float>(1,1) = -6.49408545e+02;
  P.at<float>(2,1) = -9.99867909e-01;

  P.at<float>(0,2) = 2.13725596e+03;
  P.at<float>(1,2) = 1.02711545e+01;
  P.at<float>(2,2) = -1.04081442e-02;

  P.at<float>(0,3) = 3.28415744e+01;
  P.at<float>(1,3) = 6.72734737e+02;
  P.at<float>(2,3) = -1.48406151e-01;

  
 /*
  extern cv::Mat Projection_Vector = cv::Mat(3,4, cv::CV_32F, { 2.91694788e+01, -9.97213328e+02, 2.13725596e+03, 3.28415744e+01,
-2.14379115e+03, -6.49408545e+02, 1.02711545e+01, 6.72734737e+02,
1.24834322e-02, -9.99867909e-01, -1.04081442e-02, -1.48406151e-01 });
  //need to declare rVec, tVec, K, distCoeffs
    // Decompose the projection matrix into:
*/
//note that K is the also the camera Matrix
  cv::Mat K(3,3,cv::DataType<float>::type); // intrinsic parameter matrix
  
  
  
  cv::Mat rvec(3,3,cv::DataType<float>::type); // rotation matrix
  
  cv::Mat Thomogeneous(4,1,cv::DataType<float>::type); // translation vector

  cv::decomposeProjectionMatrix(P, K, rvec, Thomogeneous);

  cv::Mat T(3,1,cv::DataType<float>::type); // translation vector
  //cv::Mat T;
  cv::convertPointsFromHomogeneous(Thomogeneous.reshape(4,1), T);

  std::cout << "K: " << K << std::endl;
  std::cout << "rvec: " << rvec << std::endl;
  std::cout << "T: " << T << std::endl;
  
  // Create distortion matrix
  cv::Mat distCoeffs(4,1,cv::DataType<float>::type);
  distCoeffs.at<float>(0) = 0;
  distCoeffs.at<float>(1) = 0;
  distCoeffs.at<float>(2) = 0;
  distCoeffs.at<float>(3) = 0;
  
  

  std::vector<cv::Point2d> projectedPoints;

  cv::Mat rvecR(3,1,cv::DataType<float>::type);//rodrigues rotation matrix
  cv::Rodrigues(rvec,rvecR);
  
  cv::projectPoints(objectPoints, rvecR, T, K, distCoeffs, projectedPoints);

  for(unsigned int i = 0; i < projectedPoints.size(); ++i)
    {
    std::cout << "Image point: " << imagePoints[i] << " Projected to " << projectedPoints[i] << std::endl;
    }

	
  float diff_x = 0;
  float diff_y = 0;
  float error = 0;
	
	//calculating the error
   for (unsigned int j = 0; j < projectedPoints.size(); ++j)
   {
	   error = 0;
	  //std::cout << "Image point: " << imagePoints[j].x << std::endl;
	  diff_x = abs(imagePoints[j].x - projectedPoints[j].x);
	  diff_y = abs(imagePoints[j].y - projectedPoints[j].y);
	  error = sqrt( (diff_x * diff_x) + (diff_y * diff_y) );
	  std::cout << "Image point: " << imagePoints[j] << " Projected to " << projectedPoints[j] << " calculated error " << error << std::endl;
	   
   }
   
  return 0;
}

   

std::vector<cv::Point2d> Generate2DPoints()
{
  std::vector<cv::Point2d> points;

  float x,y;

  x=282;y=274;
  points.push_back(cv::Point2d(x,y));

  x=397;y=227;
  points.push_back(cv::Point2d(x,y));

  x=577;y=271;
  points.push_back(cv::Point2d(x,y));

  x=462;y=318;
  points.push_back(cv::Point2d(x,y));

  x=270;y=479;
  points.push_back(cv::Point2d(x,y));

  x=450;y=523;
  points.push_back(cv::Point2d(x,y));

  x=566;y=475;
  points.push_back(cv::Point2d(x,y));
  /*
  for(unsigned int i = 0; i < points.size(); ++i)
    {
    std::cout << points[i] << std::endl;
    }
  */
  return points;
}


std::vector<cv::Point3d> Generate3DPoints()
{
  std::vector<cv::Point3d> points;

  float x,y,z;

  x=.5;y=.5;z=-.5;
  points.push_back(cv::Point3d(x,y,z));

  x=.5;y=.5;z=.5;
  points.push_back(cv::Point3d(x,y,z));

  x=-.5;y=.5;z=.5;
  points.push_back(cv::Point3d(x,y,z));

  x=-.5;y=.5;z=-.5;
  points.push_back(cv::Point3d(x,y,z));

  x=.5;y=-.5;z=-.5;
  points.push_back(cv::Point3d(x,y,z));

  x=-.5;y=-.5;z=-.5;
  points.push_back(cv::Point3d(x,y,z));

  x=-.5;y=-.5;z=.5;
  points.push_back(cv::Point3d(x,y,z));

  /*
  for(unsigned int i = 0; i < points.size(); ++i)
    {
    std::cout << points[i] << std::endl;
    }
  */
  return points;
}