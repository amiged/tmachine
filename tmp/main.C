//-----------------------------------------------------------------------------
// Output Pair-Wise Error
// Modify: Tsuyoshi Hamada, Nov, 2006
//-----------------------------------------------------------------------------
#include  <iostream>
#include  <cmath>
#include  <cstdlib>
#include  <iomanip> // cout << setw() << setprecision() 
using namespace std;

extern "C" void  force(double x[][3], double v[][3], double m[], double p[], double a[][3], double j[][3], int n);
extern "C" void _force(double x[][3], double v[][3], double m[], double p[], double a[][3], double j[][3], int n);

extern "C" void debug_position_snap(double x[][3], double Gflops, int n, int nstep);

#define NMAX 1024

double rsv[65536][3];

int main(int argc, char *argv[]) {
  int index;
  int n = 2;

  double m[NMAX];
  double r[NMAX][3];
  double v[NMAX][3];

  double p[NMAX];
  double a[NMAX][3];
  double jk[NMAX][3];

  double _p[NMAX];
  double _a[NMAX][3];
  double _jk[NMAX][3];

  m[0] = m[1] = 1.0;

  for (int i = 0; i < 3 ; i++) r[i][0] = 0.0;
  for (int i = 0; i < 3 ; i++) v[i][0] = 0.0;
  for (int i = 0; i < 3 ; i++) v[i][1] = 0.0;

  index=0;
  srand(0x12345);

  for (int t = 0; t < 1000 ; t++){
    

    //    for (int i = 0; i < 3 ; i++) r[1][i] = pow(10.0, 2.0*rand()/(RAND_MAX+1.0));



    for (int i = 0; i < 3 ; i++) r[1][i] = 1.0*rand()/(RAND_MAX+1.0);

    for (int i = 0; i < 3 ; i++)  rsv[index][i] = r[1][i];
    index++;


    _force(r, v, m, _p, _a, _jk, n);
     force(r, v, m,  p,  a,  jk, n);

     double err_p, err_a[3], err_jk[3];
     double rad;
     rad = sqrt(r[1][0]*r[1][0]+r[1][1]*r[1][1]+r[1][2]*r[1][2]);
     err_p = fabs(p[0]-_p[0])/_p[0];

    
     for (int k = 0; k < 3; k++){
       double host  = _a[0][k];
       double pipe  =  a[0][k];
       double err = sqrt((host - pipe)*(host - pipe))/host;

       cout << setw(8);
       cout.precision(6);
       cout << rad  << "\t";
       cout.precision(6);
       cout << err  << "\t";
       cout.precision(6);
       cout << host << "\t";
       cout.precision(6);
       cout << pipe << endl;

     }

  }
  

  debug_position_snap(rsv, 123.456, index, 10);

  return 0;
}
