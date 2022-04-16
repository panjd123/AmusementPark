#include <bits/stdc++.h>
#define INF 0x3f3f3f3f
#define LL long long
#define eps 1e-9
const int N=1e5+5;
using namespace std;
int n=0,m=0,T;
double data[N][M+1],x[N];
int main(){
	freopen("新数据文件.txt","r",stdin);
	for(int i=0;i<=m;i++){
		scanf("%lf",&x[i]);
		m+=(x[i]>eps);
	}
	if(m<=5) return 0;
	freopen("训练集.txt","r",stdin);
	scanf("%d",&n);
	for(int i=1;i<=n;i++){
		for(int j=0;j<=M;j++){
			scanf("%lf",&data[i][j]);
		}
	}
	freopen("训练集.txt","w",stdout);
	printf("%d\n",n+1);
	for(int i=1;i<=n;i++){
		for(int j=0;j<=M;j++){
			printf("%lf ",data[i][j]);
		}
		puts("");
		puts("");
	}
	for(int i=0;i<=M;i++) printf("%lf ",x[i]);
}

