#include <bits/stdc++.h>
#define INF 0x3f3f3f3f
#define LL long long
#define eps (1e-9)
#define ts if(1)
const int N=1e5+5,M=144,M2=2*M,P=1e8;
using namespace std;
int n,m,T,s;
bool flag;
double r,y,c,w[4][M2+1][M2+1],x[4][M2+1],f[4][M2+1],data[M+1],res;
inline double sg(double x){
	return 1.0/(1.0+exp(-x));
}
void F(){
	for(int i=2;i<=3;i++){
		for(int j=1;j<=x[i][0];j++){
			x[i][j]=w[i][j][0];
			for(int k=1;k<=x[i-1][0];k++){
				x[i][j]+=w[i][j][k]*f[i-1][k];
			}
			f[i][j]=sg(x[i][j]);
		}
	}
	int o=10; printf("%lf\n",f[3][10]);
	for(int k=1;k<=9;k++){
		if(f[3][k]>f[3][o]) o=k;
		printf("%lf\n",f[3][k]);
	}
	printf("%d",(o==10?0:o));
}
char ch[N];
int main(){
	freopen("学习结果.txt","r",stdin);
	freopen("结果文件.txt","w",stdout);
	scanf("%lf %lf",&r,&c);
	x[1][0]=M; x[2][0]=M*c; x[3][0]=s=10;
	for(int i=2;i<=3;i++){
		for(int j=1;j<=x[i][0];j++){
			for(int k=0;k<=x[i-1][0];k++){
				scanf("%lf",&w[i][j][k]);
			}
		}
	}
	freopen("新数据文件.txt","r",stdin);
	double sum=0,m=0;
	gets(ch);
	if(data[0]<eps) data[0]=s;
	for(int j=1;j<=M;j++){
		scanf("%lf",&data[j]);
		if(data[j]>eps) m++,sum+=data[j];
	}
	if(m<eps) return 0;
	sum/=m;
	for(int j=1;j<=M;j++) data[j]/=sum;
	for(int j=1;j<=M;j++) f[1][j]=x[1][j]=data[j]; 
	F();
}
