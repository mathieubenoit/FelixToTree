from ROOT import TCanvas,TTree,TH2I,TFile
from array import array
import itertools

def readfiles(foldername):

    rowfile = open("%s/fei4_ccpd_integ_row.txt"%foldername)
    colfile = open("%s/fei4_ccpd_integ_col.txt"%foldername)
    totfile = open("%s/fei4_ccpd_integ_tot.txt"%foldername)
    lv1file = open("%s/fei4_ccpd_integ_time.txt"%foldername)
    bcidfile = open("%s/fei4_ccpd_integ_bcid.txt"%foldername)
    ecidfile = open("%s/fei4_ccpd_integ_ecid.txt"%foldername)


    row = [int(line) for line in rowfile.readlines()]
    col = [int(line) for line in colfile.readlines()]
    tot = [int(line) for line in totfile.readlines()]
    lv1 = [int(line) for line in lv1file.readlines()]
    bcid = [int(line) for line in bcidfile.readlines()]
    ecid = [int(line) for line in ecidfile.readlines()]

    return row,col,tot,lv1,bcid,ecid



def buildtree(row,col,tot,lv1,bcid,ecid):

    f = TFile("FEI4_raw_file.root","recreate")
    t = TTree("Hits","Raw data tree")

    maxn=300
    row_b = array( 'i', maxn*[ 0 ] )
    col_b = array( 'i', maxn*[ 0 ] )
    tot_b = array( 'i', maxn*[ 0 ] )
    lv1_b = array( 'i', maxn*[ 0 ] )
    bcid_b = array( 'i', maxn*[ 0 ] )
    ecid_b = array( 'i', maxn*[ 0 ] )
    event_size = array('i',[0])
    hitsinCluster = array('i',[0])
    posX = array('i',[0])
    posY = array('i',[0])
    
    t.Branch( 'NHits', event_size, 'NHits/I' )
    t.Branch( 'PixY', row_b, 'PixY[NHits]/I' )
    t.Branch( 'PixX', col_b, 'PixX[NHits]/I' )
    t.Branch( 'Value', tot_b, 'Value[NHits]/I' )
    t.Branch( 'Timing', lv1_b, 'Timing[NHits]/I' )
    #t.Branch( 'bcid', bcid_b, 'bcid[event_size]/I' )
    #t.Branch( 'ecid', ecid_b, 'ecid[event_size]/I' )
    t.Branch( 'HitInCluster', event_size, 'HitInCluster/I' )
    t.Branch( 'PosX', event_size, 'PosX/I' )
    t.Branch( 'PosY', event_size, 'PosY/I' )
    t.Branch( 'PosZ', event_size, 'PosZ/I' )


    events = []
    event = []
    previous_bcid=-1
    previous_ecid=-1
    for i,bcid_t in enumerate(bcid):
        if previous_bcid == -1 :
            previous_bcid=bcid_t
            previous_ecid=ecid[i]
            event = [[row[i],col[i],tot[i],lv1[i],bcid[i],ecid[i]]]
        else:
            if abs(previous_bcid-bcid_t)<16 and previous_ecid==ecid[i]  :
                previous_bcid=bcid_t
                previous_ecid=ecid[i]
                if tot[i]==-1:
			event.append([row[i],col[i],tot[i],lv1[i],bcid[i],ecid[i]])
		else:
			event.append([row[i],col[i],tot[i],lv1[i],bcid[i],ecid[i]])
            
	    
	    else:
                events.append([ii for n,ii in enumerate(event) if ii not in event[:n]])
                previous_bcid=bcid_t
                previous_ecid=ecid[i]
                if tot[i]==-1:
			event=[[row[i],col[i],tot[i],lv1[i],bcid[i],ecid[i]]]
		else:             
			event = [[row[i],col[i],tot[i],lv1[i],bcid[i],ecid[i]]]


    ## #"""remove doubles"""
    tevents=[]
    for event in events:
        event.sort()
        tevents.append(list(event for event,_ in itertools.groupby(event)))
    events =tevents                  

    for n,event in enumerate(events):
        if n>2360 and n<2380 :
            print "event #%i"%n
        for i,hit in enumerate(event):
            if n>2360 and n<2380 :
	    	print "X:%i Y:%i bcid:%i ecid:%i tot:%i,lv1:%i"%(hit[1],hit[0],hit[4],hit[5],hit[2],hit[3])         
            row_b[i]=hit[0]
            col_b[i]=hit[1]
            tot_b[i]=hit[2]            
            lv1_b[i]=hit[3]
            bcid_b[i]=hit[4] 
            ecid_b[i]=hit[5]
        event_size[0]=len(event) 
        #print event_size
        #print row_b
        t.Fill()


 
        
    f.Write()
    f.Close()


row,col,tot,lv1,bcid,ecid = readfiles("fei4-test")
buildtree(row,col,tot,lv1,bcid,ecid)
