#include <bits/stdc++.h>
using namespace std;
const int N=1e5+5,M=144;
int n=0,m=0,t;
double data[N][M+1];
int main(){
	freopen("训练集.txt","r",stdin);
	scanf("%d",&n);
	for(int i=1;i<=n;i++){
		for(int j=0;j<=M;j++){
			scanf("%lf",&data[i][j]);
		}
	}
	freopen("删除文件.txt","r",stdin);
	scanf("%d",&t);
	freopen("删除文件.txt","w",stdout);
	if(t<=0) t=n;
	if(t>n) t=1;
	cout<<t<<" ";
	for(int j=0;j<=M;j++){
		printf("%lf ",data[t][j]);
	}
}
