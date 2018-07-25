#pragma once
#include <vector>
#include <algorithm>
#include <opencv2/highgui/highgui.hpp>

extern cv::Mat Projection_Vector = cv::Mat(3,4, cv::CV_32F, { 2.91694788e+01, -9.97213328e+02, 2.13725596e+03, 3.28415744e+01,
-2.14379115e+03, -6.49408545e+02, 1.02711545e+01, 6.72734737e+02,
1.24834322e-02 - 9.99867909e-01 - 1.04081442e-02 - 1.48406151e-01 });

extern cv::Mat Extrinsic_Vector = cv::Mat(4,4, cv::CV_32F, { 7.9138222462982188e-03, -1.0309835281602731e-02, 9.9991553578985870e-01, 8.2682261778918700e-02,
-9.9989076170250391e-01, -1.2564745997971416e-02, 7.7840747679621680e-03, 3.5556834077234029e-01,
1.2483432197947564e-02, -9.9986790850315466e-01, -1.0408144219147042e-02, -1.4840615088386888e-01,
0.0, 0.0, 0.0, 1.0 });

/*
template <typename T, typename F = boost::numeric::ublas::row_major>
boost::numeric::ublas::matrix<T, F> makeMatrix(std::size_t m, std::size_t n, const std::vector<T> & v)
{
	if (m*n != v.size()) {
		std::cout << "Size doesn't match" << std::endl;
	}
	boost::numeric::ublas::unbounded_array<T> storage(m*n);
	std::copy(v.begin(), v.end(), storage.begin());
	return boost::numeric::ublas::matrix<T>(m, n, storage);
}

boost::numeric::ublas::matrix<float> Extrinsic_Matrix = makeMatrix(4, 4, Extrinsic_Vector);
boost::numeric::ublas::matrix<float> Projection_Matrix = makeMatrix(3, 4, Projection_Vector);
*/

