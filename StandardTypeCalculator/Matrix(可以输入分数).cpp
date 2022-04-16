#include <bits/stdc++.h>
#define LL long long
#define pii pair<int,int>
#define mp make_pair
#define pb push_back
#define INF 0x3f3f3f3f
using namespace std;
const int N=1e3+5;
int T,n;
class Frac{
public:
	LL x,y;
	Frac(LL _x=0,LL _y=1){
		LL g=__gcd(_x,_y);
		if(_y<0) g=-abs(g);
		else g=abs(g);
		x=_x/g,y=_y/g;
	}
	Frac(int _x,int _y){
		int g=__gcd(_x,_y);
		if(_y<0) g=-abs(g);
		else g=abs(g);
		x=_x/g,y=_y/g;
	}
	Frac operator + (const Frac &rhs)const{
		LL _x=x*rhs.y+y*rhs.x,_y=y*rhs.y,g=__gcd(_x,_y);
		if(_y<0) g=-abs(g);
		else g=abs(g);
		return Frac(_x/g,_y/g);
	}
	Frac operator += (const Frac &rhs){
		return *this=*this+rhs;
	}
	Frac operator - (const Frac &rhs)const{
		LL _x=x*rhs.y-y*rhs.x,_y=y*rhs.y,g=__gcd(_x,_y);
		if(_y<0) g=-abs(g);
		else g=abs(g);
		return Frac(_x/g,_y/g);
	}
	Frac operator -= (const Frac &rhs){
		return *this=*this-rhs;
	}
	Frac operator * (const Frac &rhs)const{
		LL _x=x*rhs.x,_y=y*rhs.y,g=__gcd(_x,_y);
		if(_y<0) g=-abs(g);
		else g=abs(g);
		return Frac(_x/g,_y/g);
	}
	Frac operator *= (const Frac &rhs){
		return *this=*this*rhs;
	}
	Frac operator / (const Frac &rhs)const{
		LL _x=x*rhs.y,_y=y*rhs.x,g=__gcd(_x,_y);
		if(_y<0) g=-abs(g);
		else g=abs(g);
		return Frac(_x/g,_y/g);
	}
	Frac operator /= (const Frac &rhs){
		return *this=*this/rhs;
	}
	Frac operator -(){
		Frac res=*this;
		res.x*=-1;
		return res;
	}
	friend istream& operator>>(istream& in, Frac& x);
    friend ostream& operator<<(istream& out, Frac& x);
    friend ostream& operator<<(istream& out, Frac&& x);
	void out(){

	}
};
istream& operator>>(istream& in, Frac& a) {
    char s[100];
    int idx=-1;
    in >> s;
    int n=strlen(s);
    for(int i=0;i<n;i++){
		if(s[i]=='/'){
			idx=i;
			s[idx]='\0';
			break;
		}
	}
	LL _x=atoll(s),_y=1;
	if(idx!=-1) _y=atoll(s+idx+1);
	a=Frac(_x,_y);
    return in;
}
ostream& operator<<(ostream& out, Frac& a) {
	if(a.y!=1) out<<a.x<<'/'<<a.y;
	else out<<a.x;
    return out;
}
ostream& operator<<(ostream& out, Frac&& a) {
	if(a.y!=1) out<<a.x<<'/'<<a.y;
	else out<<a.x;
    return out;
    return out;
}
class Matrix{
public:
	int n,m;
	Frac a[N][N];
    friend ostream& operator<<(istream& out, Matrix& x);
    friend ostream& operator<<(istream& out, Matrix&& x);
    void out(){
    	for(int i=1;i<=n;i++){
			for(int j=1;j<=m;j++){
				cout<<a[i][j]<<'\t';
			}cout<<'\n';
		}			
    }
	void swap_r(int x,int y){
		printf("r%d <-> r%d\n",x,y);
		for(int j=1;j<=m;j++) swap(a[x][j],a[y][j]);
	}
	void swap_l(int x,int y){
		printf("c%d <-> c%d\n",x,y);
		for(int i=1;i<=n;i++) swap(a[i][x],a[i][y]);
	}
	void add_r(int x,Frac k,int y){
		cout<<"r"<<x<<" + "<<k<<" r"<<y<<endl;
		for(int j=1;j<=m;j++) a[x][j]+=a[y][j]*k;
	}
	void add_l(int x,Frac k,int y){
		cout<<"c"<<x<<" + "<<k<<" c"<<y<<endl;
		for(int i=1;i<=n;i++) a[i][x]+=a[i][y]*k;
	}
	void stdshp(){
		for(int i=1;i<=n;i++){
			if(!a[i][i].x){
				int idx=i; while(!a[i][idx].x && idx<=m) idx++;
				if(idx>m) continue;
				add_l(i,1,idx);
				add_r(i,1,idx);
				out();
			}
			for(int j=i+1;j<=m;j++){
				Frac t=-a[i][j]/a[i][i];
				add_l(j,t,i);
				add_r(j,t,i);
				out();
			}
		}
	}
}M;
ostream& operator<<(ostream& out, Matrix& mar) {
	for(int i=1;i<=mar.n;i++){
		for(int j=1;j<=mar.m;j++){
			out<<mar.a[i][j]<<'\t';
		}out<<'\n';
	}			
    return out;
}
ostream& operator<<(ostream& out, Matrix&& mar) {
	for(int i=1;i<=mar.n;i++){
		for(int j=1;j<=mar.m;j++){
			out<<mar.a[i][j]<<'\t';
		}out<<'\n';
	}			
    return out;
}
int main(){
	freopen("Mar.txt","r",stdin);
	scanf("%d",&n);
	M.n=2*n; M.m=n;
	for(int i=1;i<=n;i++) for(int j=1;j<=n;j++) cin>>M.a[i][j];
	for(int i=n+1;i<=2*n;i++) M.a[i][i-n]=1;
	M.stdshp();
}

