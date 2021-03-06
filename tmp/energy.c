#include <stdio.h>
#include <math.h>
#include "nbodysim.h"

double energy(double m[], double x[][DIM], double v[][DIM], double eps2 , int n)
{
    int i,j,d;
    double v2,r2;
    double dx[3];
    double Ep;  /* 系の位置エネルギー */
    double Em;  /* 系の運動エネルギー */
    double Ea;  /* 系の全力学的エネルギー */


    /* 系の位置エネルギー Ep を計算する。 */ 
    Ep=0.0;
    for(i=0;i<n-1;i++){
        for(j=i+1;j<n;j++){
            r2 = eps2;           /* 相対距離初期化 */
            for(d=0;d<3;d++){
                dx[d] = x[j][d] - x[i][d];
                r2 += dx[d] * dx[d];
            }
            Ep -= m[i] * m[j] * ( 1/sqrt(r2)  );
        }
    }


    /* 系の運動エネルギー Em を計算する。 */ 
    Em=0.0;
    for(i=0;i<n;i++){
        v2=0.0;    /* 絶対速度2乗値初期化 */
        for(d=0;d<3;d++){
            v2 += v[i][d]*v[i][d];
        }
        Em += 0.5 * m[i] * v2;
    }

    /* 系の全力学的エネルギー Ea を計算する。 */ 
    Ea=0.0;
    Ea = Em + Ep;

/*    printf("Emove=%1.6e,   Epot=%1.3e,   Eall=%1.25e\n",Em,Ep,Ea);*/
/*    printf("%e\n",Ea);*/

    return Ea;
}
