//-----------------------------------------------------------------------------
// mk_eight.C:  prints initial conditions for the figure eight
//              of the three-body problem
//-----------------------------------------------------------------------------
#include  <iostream>
using namespace std;

typedef double  real;                      // "real" as a general name for the
                                           // standard floating-point data type
#define  NDIM     3                        // number of spatial dimensions

int main()
{
    const int n = 3;           // number of particles
    const real t = 0;          // time
    real r[n][NDIM];           // r[i][k] : position component k for particle i
    real v[n][NDIM];           // v[i][k] : velocity component k for particle i
    real m[n];                 // m[i] : mass for particle i

    m[0] = 1;
    m[1] = 1;
    m[2] = 1;

    r[0][0] = 0.9700436;
    r[0][1] = -0.24308753;
    r[0][2] = 0;
    v[0][0] = 0.466203685;
    v[0][1] = 0.43236573;
    v[0][2] = 0;

    r[1][0] = -r[0][0];
    r[1][1] = -r[0][1];
    r[1][2] = -r[0][2];
    v[1][0] = v[0][0];
    v[1][1] = v[0][1];
    v[1][2] = v[0][2];

    r[2][0] = 0;
    r[2][1] = 0;
    r[2][2] = 0;
    v[2][0] = -2 * v[0][0];
    v[2][1] = -2 * v[0][1];
    v[2][2] = -2 * v[0][2];

    cout.precision(16);

    cout << n << endl;                      // first output line:  N
    cout << t << endl;                      // second output line:  time
    for (int i = 0; i < n; i++){
        cout << m[i];                       // each next output line:
        for (int k = 0; k < NDIM; k++)      //   m r_x r_y r_z v_x v_y v_z
            cout << ' ' << r[i][k];
        for (int k = 0; k < NDIM; k++)
            cout << ' ' << v[i][k];
        cout << endl;
    }
}
//-----------------------------------------------------------------------------
