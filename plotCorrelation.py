from ROOT import TCanvas,TTree,TH2I,TFile
from array import array




def PlotCorrelation(file1,file2):


    f = TFile(file1,"open")
    f2= TFile(file2,"open")

    f.cd()
    t = f.Get("Plane0/Hits")
    f2.cd()
    t2= f2.Get("Hits")

    t.Print()
    t2.Print()

    t2.AddFriend(t)

    histoxx = TH2I("corxx","corxx",80,0,80,80,0,80)
    histoxy = TH2I("corxy","corxy",80,0,80,336,0,336)
    histoyx = TH2I("coryx","coryx",336,0,336,80,0,80)
    histoyy = TH2I("coryy","coryy",336,0,336,336,0,336)

    nevent = t2.GetEntriesFast()

    for i in range(nevent):
        t.GetEntry(i)
        t2.GetEntry(i)

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

    can.SaveAs("correlation_plane0_DUT.png")
    a=raw_input()
    return histoxx,histoxy,histoyx,histoyy
        


histox=PlotCorrelation("cosmic_007064.root","FEI4_raw_file.root")

