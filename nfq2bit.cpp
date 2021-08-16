#include <iostream>
#include <cstdlib>
#include <ctime>

#include <stdint.h>
 
#include <string>
#include <fstream>
#include <vector>
#include <stdlib.h>
#include<sys/time.h>
#include <netinet/in.h>
#include <linux/types.h>
using namespace std;
 
extern "C" {
#include <linux/netfilter.h>
#include <linux/netfilter/nfnetlink.h>
#include <linux/netfilter/nfnetlink_queue.h>
#include <libnetfilter_queue/libnetfilter_queue.h>
}typedef unsigned char BYTE;
 
 
void swap(char *x, char *y);
char* permute(char *a, int l, int r);
float getNumbers(char* s);

std::vector<double> readFromFile();
std::vector<string> readPerm(string name);
int insertFinger(string data);
int rollDie();
static int cb(struct nfq_q_handle *qh, struct nfgenmsg *nfmsg,
        struct nfq_data *nfa, void *data);
static u_int32_t prinft_pkt(struct nfq_data *tb);
using std::cout;
std::vector<string> perm0=readPerm("permutations/perm0.txt");
std::vector<string> perm1=readPerm("permutations/perm1.txt");

std::vector<double> fingerprint =readFromFile();
int currentMarkInterval = 0;
 
int countB=-1;
int currentMark=0;
int finger=0;
int random_num=0;
int countFinger=0;
int count=0;
int intervalLength =2160;
int subintervalLength =120;
int numberofSubintervals = intervalLength / subintervalLength;
int numberOfSlots = 6;
double mslotLength =20;// subintervalLength / numberOfSlots;

long int previousTime=0;
long int initialTime = 0;
 
int main(void) {
 
 
    struct nfq_handle *h;
    struct nfq_q_handle *qh;
    struct nfnl_handle *nh;

	//fprintf("%d \n",fingerprint[0]);
 	//cout<<"Hey"<<fingerprint[0];
    int fd;
    int rv;
    char buf[4096] __attribute__ ((aligned));
 
    std::cout << "Hey you!" << perm1.size() << "  " << perm0.size()
            << "   " << fingerprint.size() <<"  " << mslotLength<<endl;
 
    struct timeval tr;
    gettimeofday(&tr, NULL);
    initialTime = tr.tv_sec * 1000 + tr.tv_usec / 1000;
cout<<"Parameters:   "<<intervalLength<<"   "<<subintervalLength<<"  "<<numberofSubintervals<<"   "<<numberOfSlots<<"   "<<mslotLength;
    h = nfq_open();
    qh = nfq_create_queue(h, 1, &cb, NULL);
 
    if (!qh) {
        fprintf(stderr, "error during nfq_create_queue()\n");
        //exit(1);
    }
 
    printf("setting copy_packet mode\n");
    if (nfq_set_mode(qh, NFQNL_COPY_PACKET, 0xffff) < 0) {
        fprintf(stderr, "can't set packet_copy mode\n");
        //exit(1);
    }
 
    fd = nfq_fd(h);
 
    while ((rv = recv(fd, buf, sizeof(buf), 0)) && rv >= 0) {
        //printf("pkt received\n");
        nfq_handle_packet(h, buf, rv);
    }
 
    printf("unbinding from queue 0\n");
    nfq_destroy_queue(qh);
 
#ifdef INSANE
    /* normally, applications SHOULD NOT issue this command, since
     * it detaches other programs/sockets from AF_INET, too ! */
    printf("unbinding from AF_INET\n");
    nfq_unbind_pf(h, AF_INET);
#endif
 
    printf("closing library handle\n");
    nfq_close(h);
 
    //exit(0);
 
    //getNumbers(s);
    //std::vector <double> arr = readFromFile();
    //std::vector<string> arr2 = readPermFromFile("perm.txt");
 
    //insertFinger("hey");
 
    return 0;
 
}
static u_int32_t prinft_pkt(struct nfq_data *tb) {
    int id = 0;
    struct nfqnl_msg_packet_hdr *ph;
    struct nfqnl_msg_packet_hw *hwph;
    u_int32_t mark, ifi;
    int ret;
    unsigned char *data;
 
    ph = nfq_get_msg_packet_hdr(tb);
    if (ph) {
        id = ntohl(ph->packet_id);
        //printf("hw_protocol=0x%04x hook=%u id=%u ", ntohs(ph->hw_protocol),
        //      ph->hook, id);
    }
 
    hwph = nfq_get_packet_hw(tb);
    ret = nfq_get_payload(tb, &data);
         
    //data = (unsigned char*)"hello";
 
    //strcmp
    //printf(">> %s\n", data);  //if (ret >= 0)
    /*BYTE byteArray[3] = data;//{ 0x48, 0x65, 0x6C, 0x6C, 0x6F };
    std::string s(reinterpret_cast<char*>(byteArray), sizeof(byteArray));
    std::cout << s << std::endl;*/
 
    //  printf("payload_len=%d ", ret);
 
    fputc('\n', stdout);
 
    return id;
}
static int cb(struct nfq_q_handle *qh, struct nfgenmsg *nfmsg,
        struct nfq_data *nfa, void *data) {
    u_int32_t id = prinft_pkt(nfa);
 
    //printf("entering callback\n");
 
    insertFinger("hey you");
 
    return nfq_set_verdict(qh, id, NF_ACCEPT, 0, NULL);
}
int insertFinger(string data) {
    struct timeval tp;
    gettimeofday(&tp, NULL);
    int index = 0;
    long int ms = tp.tv_sec * 1000 + tp.tv_usec / 1000;
    long int relativeTime = ms - initialTime;
    index=relativeTime/intervalLength;
    int lenn = 30;
    long int currentTime = tp.tv_sec * 1000 + tp.tv_usec / 1000;
    relativeTime = currentTime - initialTime;
    //int prevL=relativeTime;
/*int randMove=rand()%10;
if (randMove<4){
cout<<"do not move";
return 1;}*/

    while (relativeTime < intervalLength * lenn * 200) {
		
		
	struct timeval tpr;
        gettimeofday(&tpr, NULL);
        currentTime = tpr.tv_sec * 1000 + tpr.tv_usec / 1000;
        index = int((currentTime - initialTime) / intervalLength);
        relativeTime = currentTime - initialTime;
 
 
        if (count==0 || relativeTime - previousTime >= 9*1000) {
            cout<<"End is found";
            count += 1;
 
            initialTime = currentTime;
            currentMark = -1;
            index = 0;
            countFinger += 1;
            relativeTime = currentTime - initialTime;
 
            //target.write(str(count)+" ")
            //payload.set_verdict(nfqueue.NF_ACCEPT)
 
        }
        if (index >= lenn) {
 
            //cout << "Sent packet without Fingerprint";
            //payload.set_verdict(nfqueue.NF_ACCEPT)
            previousTime=relativeTime;
            return 1;
 
        }
	previousTime=relativeTime;
        if (countB != index) {
             
            currentMark += 1;
 	    srand(time(NULL));
            random_num = rand() % 6;//random.randrange(0,numberOfSlots/2);
            finger =fingerprint[index];

            cout<<"\nCurrent Mark Interval:  "<<currentMark<<"   "<<finger<<endl<<std::flush;
 
 
        }
        countB = index;
 
        int currentSubinterval = int((relativeTime - index * intervalLength) / (subintervalLength));
 
        int location = perm0[(index * numberofSubintervals + currentSubinterval)][random_num]-'0';
        int val = ((relativeTime) - index * intervalLength- currentSubinterval * subintervalLength);
        int currentSlot = int(val / ((mslotLength)));
        //cout<<currentSubinterval<<"   "<<location<<"  "<<currentSlot<<endl<<std::flush;
        if (finger == 1) {
            location =perm1[index * numberofSubintervals
                + currentSubinterval][random_num]-'0';
 
        }

	
        if (currentSlot == location) {
            cout << "Approve Packet in Mark Interval     " << relativeTime<<"   "
                    << numberofSubintervals;
            if (currentSubinterval == numberofSubintervals - 1) {       //?????
                currentMarkInterval += 1;
 
            }
            //payload.set_verdict(nfqueue.NF_ACCEPT)
            break;
 
        } else if (currentSlot > location
                && currentSubinterval == numberofSubintervals - 1) {
            //payload.set_verdict(nfqueue.NF_ACCEPT)
            cout << "Packets in the last Subinterval Of mark interval     "
                    << relativeTime;
            return 1;
 
        }
 
    }
    return 0;
 
}
void swap(char *x, char *y) {
    char temp;
    temp = *x;
    *x = *y;
    *y = temp;
}
 
/* Function to print permutations of string
 This function takes three parameters:
 1. String
 2. Starting index of the string
 3. Ending index of the string. */
char* permute(char *a, int l, int r) {
    int i;
    if (l == r)
        printf("%s\n", a);
    else {
        for (i = l; i <= r; i++) {
            swap((a + l), (a + i));
            permute(a, l + 1, r);
            swap((a + l), (a + i)); //backtrack
        }
    }
 
    return a;
}/*
 float getNumbers(char* num) {
 
 int len = 0;
 len = strlen(num);
 int result = atoi(num);
 printf("%f", strtod(num, NULL));
 return strtod(num, NULL);
 
 
 }*/
 
std::vector<string> readPerm(string filename) {
    std::ifstream in(filename.c_str());
    string num;
    std::vector<string> result;
    while (in >> num) {
        result.push_back(num);
    }
    return result;
}
int rollDie(){
    return 0;
}
std::vector<double> readFromFile() {
    std::ifstream in("FingerPrintConv.txt");
    double num;
    std::vector<double> result;
    std::vector<double> resultStr;
    while (in >> num) {
        result.push_back(num);
    }
 for (int i = 0; i < result.size(); ++i) {
        std::cout << result[i]<<" ";
    }



	/*for (int i=0; i<=29;i+=2){
		int a=0;
		a=(result[0][i]-'0')*2;

		a+=(result[0][i+1]-'0');
	
		resultStr.push_back(a);

}for (int i = 0; i < resultStr.size(); ++i) {
        std::cout <<"Bef:    "<< resultStr[i]<<" ";
    }*/

    return result;
}
