#include <bits/stdc++.h>
using namespace std;
const int N=1e5+5,M=144;
int n=0,m=0,t;
double data[N][M+1];
int main(){
	freopen("ѵ����.txt","r",stdin);
	scanf("%d",&n);
	for(int i=1;i<=n;i++){
		for(int j=0;j<=M;j++){
			scanf("%lf",&data[i][j]);
		}
	}
	freopen("ɾ���ļ�.txt","r",stdin);
	scanf("%d",&t);
	freopen("ѵ����.txt","w",stdout);
	cout<<n-1<<endl;
	for(int i=1;i<=n;i++)if(i!=t){
		for(int j=0;j<=M;j++){
			printf("%lf ",data[i][j]);
		}
		puts("");
	}
}
