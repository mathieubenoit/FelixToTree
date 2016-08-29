from ROOT import TCanvas,TTree,TH2I,TFile
from array import array




def PlotRawResidual(file1,file2,plane=0,offset=0):

    f = TFile(file1,"open")
    f2= TFile(file2,"open")

    f.cd()
    t = f.Get("Plane%i/Hits"%plane)
    f2.cd()
    t2= f2.Get("Hits")

    t.Print()
    t2.Print()
    print offset
    #t2.AddFriend(t)


    nevent = t2.GetEntriesFast()


    histoxx = TH2I("corxx","corxx",nevent/1,0,nevent,2*336,-336*50,336*50 )
    histoxy = TH2I("corxy","corxy",nevent/1,0,nevent,2*336,-336*50,336*50)



    imin=0
    imax=0
    if offset>=0:
        imin=0
        imax=nevent-offset
    else:
        imin=abs(offset)
        imax=nevent

    for i in range(imin,imax):
        t.GetEntry(i)
        t2.GetEntry(i+offset)
#               for x in t.PixX:
#                       for xx in t2.PixX:
#                 #print x,xx
#                               histoxx.Fill(i,x*250-xx*250)
        for x in t.PixX:
            for xx in t2.PixY:
      #print x,xx
                histoxy.Fill(i,x*250-xx*50)

    can= TCanvas()
#       can.Divide(2,1)

#       can.cd(1)
#       histoxx.Draw("colz")
#       can.cd(2)
    histoxy.Draw("colz")
    a = raw_input()
    can.SaveAs("correlation_vs_offset.png")


def PlotCorrelation(file1,file2,plane=0,offset=0):


    f = TFile(file1,"open")
    f2= TFile(file2,"open")

    f.cd()
    t = f.Get("Plane%i/Hits"%plane)
    f2.cd()
    t2= f2.Get("Hits")

    t.Print()
    t2.Print()
    t2.AddFriend(t)
    histoxx = TH2I("corxx","corxx",80,0,80,80,0,80)
    histoxy = TH2I("corxy","corxy",80,0,80,336,0,336)
    histoyx = TH2I("coryx","coryx",336,0,336,80,0,80)
    histoyy = TH2I("coryy","coryy",336,0,336,336,0,336)

    if t2.GetEntriesFast() > t.GetEntriesFast():

        nevent = t.GetEntriesFast()
    else:
        nevent = t2.GetEntriesFast()

    imin=0
    imax=nevent
    if offset>=0:
        imin=0
        imax=nevent-offset
    else:
        imin=abs(offset)
        imax=nevent

    for i in range(imin,imax):
        t.GetEntry(i)
        t2.GetEntry(i+offset)

        for x in t.PixX:
            for xx in t2.PixX:
        #print x,xx
                histoxx.Fill(x,xx)
        for x in t.PixX:
            for xx in t2.PixY:
                #print x,xx
                histoxy.Fill(x,xx)
        for x in t.PixY:
            for xx in t2.PixX:
                #print x,xx
                histoyx.Fill(x,xx)
        for x in t.PixY:
            for xx in t2.PixY:
                #print x,xx
                histoyy.Fill(x,xx)

    can= TCanvas()
    can.Divide(2,2)

    can.cd(1)
    histoxx.Draw("colz")
    can.cd(2)
    histoxy.Draw("colz")
    can.cd(3)
    histoyx.Draw("colz")
    can.cd(4)
    histoyy.Draw("colz")
    a = raw_input()
    can.SaveAs("correlation_plane%i_DUT.png"%plane)
    return histoxx,histoxy,histoyx,histoyy


#for i in range(-20,20,1):
#histos=PlotCorrelation("fei4-test/cosmic_007092.root","FEI4_raw_file.root",0)
h=0
for i in range(-2,4,1):
	h=PlotRawResidual("fei4-test/cosmic_007105.root","FEI4_raw_file.root",0,i)
