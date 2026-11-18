// No72 independent 3-cop exact game check using precomputed CSR transitions,
// in contrast to the on-the-fly state successor solver.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
struct B {
 uint64_t bit[3]{};
 inline void insert(int i){bit[i/64] |= uint64_t(1)<<(i%64);}
 inline void merge(const B&b){for(int i=0;i<3;i++)bit[i]|=b.bit[i];}
 inline bool covers(const B&b)const{for(int i=0;i<3;i++)if((b.bit[i]&~bit[i])!=0)return false;return true;}
 inline int count()const{return popcount(bit[0])+popcount(bit[1])+popcount(bit[2]);}
 bool operator==(const B&b)const{return bit[0]==b.bit[0] && bit[1]==b.bit[1] && bit[2]==b.bit[2];}
};
int main(int argc,char**argv){
 int n=argc>1?atoi(argv[1]):10,depth=argc>2?atoi(argv[2]):5;
 if(n>10 || n<1){cerr<<"n out of range\n";return 2;}
 vector<int> v;for(int x=0;x<(1<<n);x++)if(!(x&(x>>1)))v.push_back(x);
 int N=v.size();
 vector<vector<int>> ne(N);
 vector<B> nb(N);
 for(int i=0;i<N;i++)for(int j=0;j<N;j++)if(popcount((unsigned)(v[i]^v[j]))<=1){ne[i].push_back(j);nb[i].insert(j);}
 vector<array<uint8_t,3>> starts;
 vector<int> lookup(N*N*N,-1);
 for(int i=0;i<N;i++)for(int j=i;j<N;j++)for(int k=j;k<N;k++){
  lookup[(i*N+j)*N+k]=starts.size();starts.push_back({uint8_t(i),uint8_t(j),uint8_t(k)});
 }
 int S=starts.size();
 vector<uint32_t> offsets(S+1);
 vector<uint32_t> targets;
 targets.reserve(size_t(S)*400);
 for(int s=0;s<S;s++){
  auto q=starts[s];
  for(int a:ne[q[0]])for(int b:ne[q[1]])for(int c:ne[q[2]]){
    array<int,3> w={a,b,c}; sort(w.begin(),w.end());
    int dst=lookup[(w[0]*N+w[1])*N+w[2]];
    if(dst<0){cerr<<"bad successor\n";return 3;}
    targets.push_back(uint32_t(dst));
  }
  offsets[s+1]=targets.size();
 }
 cout<<"n="<<n<<" vertices="<<N<<" states="<<S<<" transitions="<<targets.size()<<"\n"<<flush;
 ofstream winner_output;
 if(argc>=4){winner_output.open(argv[3]);winner_output<<"c0,c1,c2\n";}
 vector<B> occupied(S),wins(S),post(S),old(S);
 for(int s=0;s<S;s++){
  for(uint8_t x:starts[s])occupied[s].insert(x);
  wins[s]=occupied[s];
 }
 B universe;for(int x=0;x<N;x++)universe.insert(x);
 for(int t=1;t<=depth;t++){
   for(int s=0;s<S;s++){
     B next=occupied[s];
     for(int r=0;r<N;r++)if(wins[s].covers(nb[r]))next.insert(r);
     post[s]=next;
   }
   int maxN=0,champions=0;
   for(int s=0;s<S;s++){
     B next;
     for(uint32_t e=offsets[s];e<offsets[s+1];e++)next.merge(post[targets[e]]);
     old[s]=next;
     maxN=max(maxN,next.count());
     if(next==universe){
      champions++;
      if(t==depth && winner_output){auto q=starts[s];winner_output<<v[q[0]]<<","<<v[q[1]]<<","<<v[q[2]]<<"\n";}
     }
   }
   cout<<"t="<<t<<" max="<<maxN<<"/"<<N<<" winners="<<champions<<"\n"<<flush;
   wins.swap(old);
 }
}
