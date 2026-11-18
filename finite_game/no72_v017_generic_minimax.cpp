// No72. Exact 3-cop full alternating game on Gamma_n, 1<=n<=10.
// Independently implemented, without storing police transition graph.
// Cops place, robber places, police move (each one step or still), robber moves.
#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <vector>
using namespace std;
struct M {
 uint64_t a=0,b=0,c=0;
 inline void add(int v){if(v<64)a|=uint64_t(1)<<v;else if(v<128)b|=uint64_t(1)<<(v-64);else c|=uint64_t(1)<<(v-128);}
 inline void merge(const M&v){a|=v.a;b|=v.b;c|=v.c;}
 inline bool incl(const M&v)const{return (a&v.a)==v.a&&(b&v.b)==v.b&&(c&v.c)==v.c;}
 inline bool operator==(const M&v)const{return a==v.a&&b==v.b&&c==v.c;}
 inline int cnt()const{return popcount(a)+popcount(b)+popcount(c);}
};
int main(int argc,char**argv){
 const int n=argc>1?atoi(argv[1]):9,depth=argc>2?atoi(argv[2]):5;
 if(n<1||n>10||depth<0){cerr<<"arguments: n<=10, depth>=0\n";return 1;}
 vector<int> vertex;for(int x=0;x<(1<<n);x++)if((x&(x>>1))==0)vertex.push_back(x);
 const int N=vertex.size();
 vector<vector<int>> move(N);
 vector<M> closed(N);
 for(int i=0;i<N;i++)for(int j=0;j<N;j++) if(popcount((unsigned)(vertex[i]^vertex[j]))<=1){move[i].push_back(j);closed[i].add(j);}
 vector<array<uint8_t,3>> triples;
 vector<int> index(N*N*N,-1);
 for(int i=0;i<N;i++)for(int j=i;j<N;j++)for(int k=j;k<N;k++){index[(i*N+j)*N+k]=triples.size();triples.push_back({(uint8_t)i,(uint8_t)j,(uint8_t)k});}
 const int S=triples.size();
 vector<M> occupied(S), win(S), robust(S), winNew(S);
 for(int s=0;s<S;s++){auto t=triples[s];for(int i:t)occupied[s].add(i);win[s]=occupied[s];}
 M full;for(int i=0;i<N;i++)full.add(i);
 cout<<"n="<<n<<" V="<<N<<" cop_starts="<<S<<"\n"<<flush;
 for(int turn=1;turn<=depth;turn++){
  auto t0=chrono::steady_clock::now();
  for(int s=0;s<S;s++){
   M good=occupied[s];
   for(int r=0;r<N;r++) if(win[s].incl(closed[r]))good.add(r);
   robust[s]=good;
  }
  int champions=0,most=0;array<int,3> unique{-1,-1,-1};
  for(int s=0;s<S;s++){
   auto q=triples[s];M favorable;
   for(int i:move[q[0]])for(int j:move[q[1]])for(int k:move[q[2]]){
    int a=i,b=j,c=k;
    if(a>b)swap(a,b);if(b>c)swap(b,c);if(a>b)swap(a,b);
    const int dst=index[(a*N+b)*N+c];assert(dst>=0);
    favorable.merge(robust[dst]);
    if(favorable==full)goto early_done;
   }
   early_done:
   winNew[s]=favorable;
   most=max(most,favorable.cnt());
   if(favorable==full){champions++;auto t=triples[s];unique={vertex[t[0]],vertex[t[1]],vertex[t[2]]};}
  }
  win.swap(winNew);
  auto dt=chrono::duration<double>(chrono::steady_clock::now()-t0).count();
  cout<<"turn="<<turn<<" max_win_start="<<most<<"/"<<N<<" universal="<<champions<<" time_s="<<fixed<<setprecision(3)<<dt;
  if(champions==1)cout<<" unique="<<unique[0]<<","<<unique[1]<<","<<unique[2];
  cout<<"\n"<<flush;
 }
}
