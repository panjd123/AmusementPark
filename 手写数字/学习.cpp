#include <bits/stdc++.h>
#define INF 0x3f3f3f3f
#define LL long long
#define eps (1e-9)
#define ts if(1)
const int N=1e5+5,M=144,M2=2*M,P=1e8;
using namespace std;
int n,m,T,s,cnt[50];
bool flag,TS;
double r,c,y,dy,w[4][M2+1][M2+1],w0[4][M2+1][M2+1],x[4][M2+1],f[4][M2+1],data[N][M+1],d[M2+1],e[M2+1],res;
int yz[N],zq[N];
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
	int o=0;
	for(int k=1;k<=10;k++){
		if(f[3][k]>f[3][o]) o=k;
		dy=((y==k?1:0)-f[3][k])*((y==k?1:0)-f[3][k]);
	}
	res+=(abs(o-y)<eps);
	if(abs(o-y)<eps) zq[(o==10?0:o)]++;
}
void F_rev(){
	for(int k=1;k<=x[3][0];k++){
		d[k]=((y==k?1:0)-f[3][k])*f[3][k]*(1-f[3][k]);
	}
	for(int j=1;j<=x[2][0];j++){
		e[j]=0;
		for(int k=1;k<=x[3][0];k++){
			e[j]+=w[3][k][j]*d[k];
		}
		e[j]*=f[2][j]*(1-f[2][j]);
	}
	for(int k=1;k<=x[3][0];k++){
		for(int j=1;j<=x[2][0];j++){
			w[3][k][j]+=r*d[k]*f[2][j];
			//w0[3][k][j]+=r*d[k]*f[2][j];
		}
		w[3][k][0]+=r*d[k];
		//w0[3][k][0]+=r*d[k];
	}
	for(int j=1;j<=x[2][0];j++){
		for(int i=1;i<=x[1][0];i++){
			w[2][j][i]+=r*e[j]*f[1][i];
			//w0[2][j][i]+=r*e[j]*f[1][i];
		}
		w[2][j][0]+=r*e[j];
		//w0[2][j][0]+=r*e[j];
	}
}
void F_rev_lst(){
	return ;
	for(int i=2;i<=3;i++){
		for(int j=1;j<=x[i][0];j++){
			for(int k=0;k<=x[i-1][0];k++){
				w[i][j][k]+=w0[i][j][k]/n;
			}
		}
	}
}
void out_data(){
	for(int i=1;i<=n;i++){
		int t=1;
		cout<<data[i][0]<<endl;
		for(int j=1;j<=8;j++){
			for(int k=1;k<=7;k++){
				cout<<data[i][t++]<<" ";
			}cout<<endl;
		}
	}
}
double rd(double a,double b){
	int x=rand(),l=(b-a)*100; x=x%l;
	return (a+b)/2+(x-l/2)/100.0;
}
int main(){
	freopen("训练集.txt","r",stdin);
	//初值 
	r=0.1; c=0.11; s=10;
	srand(20210126);
	//srand(time(NULL));
	for(int i=1;i<=3;i++){
		for(int j=0;j<=M2;j++){
			w[i][j][0]=rd(-1,0);
			for(int k=1;k<=M2;k++){
				w[i][j][k]=rd(-1,1);
			}
		}
	}
	x[1][0]=M; x[2][0]=M*c; x[3][0]=s;//勿改 
	//读入训练集 
	scanf("%d",&n); 
	for(int i=1;i<=n;i++){
		double sum=0,m=0;
		scanf("%lf",&data[i][0]); cnt[int(data[i][0]+eps)]++;
		if(data[i][0]<eps) data[i][0]=s;
		for(int j=1;j<=M;j++){
			scanf("%lf",&data[i][j]);
			if(data[i][j]>eps){
				m++,sum+=data[i][j];
			} 
		}
		if(m==0){
			continue;
			data[i][0]=11;
		}
		sum/=m;
		for(int j=1;j<=M;j++) data[i][j]/=sum;
	}
	//机器学习 
	dy=1e9;
	int nn=1000000000/n/(M*M*c+M*c*10);
	T=nn;
	while(T--){
		if(dy<1e-5 && res/n>0.98) break;
		flag=0;
		res=0;
		for(int i=1;i<=n;i++){
			y=data[i][0];
			for(int j=1;j<=M;j++) f[1][j]=x[1][j]=data[i][j];
			F(); F_rev(); //F_rev_lst();
			if(res/n>=0.95) r=0.03;
		}
		if((nn-T)%25==0)cerr<<"第"<<nn-T<<"轮学习完成度:"<<res<<"/"<<n<<"   代价函数值:"<<dy<<" 轮数上限:"<<nn<<endl;
		//F_rev_lst();
	}
	//验证 
	freopen("验证集.txt","r",stdin);
	res=0;
	memset(zq,0,sizeof zq);
	scanf("%d",&n);
	for(int i=1;i<=n;i++){
		double sum=0,m=0;
		scanf("%lf",&y); yz[int(y)]++; if(y<eps) y=s;
		for(int j=1;j<=M;j++){
			scanf("%lf",&x[1][j]);
			if(x[1][j]>eps) m++,sum+=x[1][j];
		}
		if(m<eps) continue;
		sum/=m;
		for(int j=1;j<=M;j++) f[1][j]=x[1][j]=x[1][j]/sum;
		F();
	}
	cerr<<"测试集正确率:"<<res<<"/"<<n<<endl;
	//输出正确率 
	freopen("状态文件.txt","w",stdout);
	cout<<res<<"/"<<n<<" ";
	for(int i=0;i<=9;i++) cout<<i<<":"<<zq[i]<<"/"<<yz[i]<<endl;
	cout<<" "; 
	for(int i=0;i<=9;i++) cout<<i<<":"<<cnt[i]<<"个"<<endl; 
	//输出参数 
	freopen("学习结果.txt","w",stdout);
	printf("%.10lf %.10lf\n",r,c);
	for(int i=2;i<=3;i++){
		for(int j=1;j<=x[i][0];j++){
			for(int k=0;k<=x[i-1][0];k++){
				printf("%.10lf ",w[i][j][k]);
			}
		}
	}
}
