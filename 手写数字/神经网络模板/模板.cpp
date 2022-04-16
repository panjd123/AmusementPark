#include <bits/stdc++.h>
#define DB double
#define I inline
#define eps 1e-8
using namespace std;
const int N=1000;
I DB sg(DB x){return 1/(1+exp(-x));}
I DB th(DB x){return (exp(2*x)-1)/(exp(2*x)+1);}
I DB ReLU(DB x){return x>=0?x:0;}
I DB rd(DB a,DB b){
	int x=rand(),l=(b-a)*100; x=x%l;
	return (a+b)/2+(x-l/2)/100.0;
}
struct DATA{
	DB x[N],y;
	void r(int m){
		scanf("%lf",&y);
		for(int i=1;i<=m;i++) scanf("%lf",&x[i]);
	}
}data[N];
struct ANS{
	DB x[N];
	void out(DATA a){
		printf("期望结果:%d\n",int(a.y));
		for(int i=1;i<=10;i++) cout<<i<<" "<<x[i]<<endl;
		puts("----------------------");
	}
	int mx(int m){
		int res=1;
		for(int i=1;i<=m;i++) if(x[res]>x[i]) res=i;
		return res;
	}
}ans[N];
struct NULEV{
	int n,id;
	NULEV *pre,*nxt;
	DB w[N][N],x[N],f[N],e[N];
	void set(int _id,NULEV *_pre,NULEV *_nxt){
		id=_id; pre=_pre; nxt=_nxt;
		memset(x,0,sizeof x);
		memset(f,0,sizeof f);
		memset(e,0,sizeof e);
		for(int i=1;i<=n;i++)
			for(int j=0;j<=pre->n;j++)
				w[i][j]=rd(-1,1);
	}
	void fill(DATA a){for(int i=1;i<=n;i++) f[i]=x[i]=a.x[i];}
	void set_wi_r(){
		for(int i=1;i<=n;i++)
			for(int j=0;j<=pre->n;j++)
				scanf("%lf",&w[i][j]);
	}
	void cal(){
		for(int i=1;i<=n;i++){
			x[i]=w[i][0]; for(int j=1;j<=pre->n;j++) x[i]+=pre->f[j]*w[i][j];
		}
		if(id==1){//sigmoid
			for(int i=1;i<=n;i++) f[i]=sg(x[i]);
		}
		else if(id==2){//softmax
			DB sum=0;
			for(int i=1;i<=n;i++) sum+=exp(x[i]);
			for(int i=1;i<=n;i++) f[i]=exp(x[i])/sum;
		}
		else if(id==3){//tanh
			for(int i=1;i<=n;i++) f[i]=th(x[i]);
		}
		else if(id==4){//ReLU
			for(int i=1;i<=n;i++) f[i]=ReLU(x[i]);
		}
	}
	void adj_s(DATA a){
		DB y=a.y;
		for(int i=1;i<=n;i++) e[i]=((i==y)-f[i]);
	}
	void adj(DB r){
		for(int j=1;j<=pre->n;j++) pre->e[j]=0;
		for(int i=1;i<=n;i++){
			if(id==1 || id==2) e[i]*=f[i]*(1-f[i]);
			else if(id==3) e[i]*=(1-f[i]*f[i]);
			else if(id==4) e[i]*=(f[i]>0?1:0);
			w[i][0]+=r*e[i];
			for(int j=1;j<=pre->n;j++){
				pre->e[j]+=w[i][j]*e[i];
				w[i][j]+=r*e[i]*pre->f[j];
			}
		}
	}
	void test(){
		for(int i=1;i<=n;i++) printf("%lf ",x[i]);
	}
};
struct NUNET{
	int n,m,s;
	DB c,r;
	NULEV lev[10];
	void set(int _n,int _m,int _s,DB _c,DB _r){
		n=_n,m=_m,s=_s,c=_c,r=_r;
		lev[1].n=m;
		lev[n].n=s;
		for(int i=2;i<n;i++) lev[i].n=m*c;
		//激活函数类型 
		for(int i=1;i<=n;i++) lev[i].set(1,&lev[i-1],&lev[i+1]);
		lev[1].id=0; lev[s].id=2;
	}
	void set_wi_r(){
		for(int i=1;i<=n;i++) lev[i].set_wi_r();
	}
	int f(DATA a,ANS &ans){
		lev[1].fill(a);
		for(int i=2;i<=n;i++){
			lev[i].cal();
		}
		for(int i=1;i<=s;i++) ans.x[i]=lev[n].f[i];
		return ans.mx(10)==a.y;
	}
	void f_rev(DATA a){
		lev[n].adj_s(a);
		for(int i=n;i>1;i--) lev[i].adj(r);
	}
}NET;
int n,m=144,lev_n=3,lrn_t=100;
int main(){
	freopen("训练集.txt","r",stdin); 
	scanf("%d",&n); for(int i=1;i<=n;i++) data[i].r(m);
	NET.set(lev_n,m,10,0.1,0.1);//n,m,s,c,r
	while(lrn_t--){
		int sum=0;
		for(int i=1;i<=n;i++){
			sum+=NET.f(data[i],ans[i]);
			NET.f_rev(data[i]);
		}
		cout<<sum<<"/"<<n<<endl;
	}
}
