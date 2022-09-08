// -*- C++ -*-
//
// Package:    Hcal4DQMAnalyzer/Hcal4DQMAnalyzer
// Class:      Hcal4DQMAnalyzer
//
/**\class Hcal4DQMAnalyzer Hcal4DQMAnalyzer.cc Hcal4DQMAnalyzer/Hcal4DQMAnalyzer/plugins/Hcal4DQMAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Long Wang
//         Created:  Thu, 12 Aug 2021 12:32:06 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/HcalDetId/interface/HcalSubdetector.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/HcalDetId/interface/HcalGenericDetId.h"
#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "DataFormats/EcalDigi/interface/EcalDigiCollections.h"
#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/HcalRecHit/interface/CaloRecHitAuxSetter.h"
#include "DataFormats/HcalRecHit/test/HcalRecHitDump.cc"

#include "CalibFormats/HcalObjects/interface/HcalDbService.h"
#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"
#include "CalibFormats/HcalObjects/interface/HcalCoderDb.h"

#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"

#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include "TTree.h"
#include "TNtuple.h"

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.


class Hcal4DQMAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit Hcal4DQMAnalyzer(const edm::ParameterSet&);
      ~Hcal4DQMAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      edm::EDGetTokenT<QIE11DigiCollection> qie11digisToken_;
      edm::ESGetToken<HcalDbService, HcalDbRecord> hcalDbServiceToken_;
      const HcalDbService* conditions;

      TH3I* hist3D_depth1;
      TH3I* hist3D_depth2;
      TH3I* hist3D_depth3;
      TH3I* hist3D_depth4;
      TH3I* hist3D_depth5;
      TH3I* hist3D_depth6;
      TH3I* hist3D_depth7;

      TTree* evttree;
      int RunNum;
      int LumiSec;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
Hcal4DQMAnalyzer::Hcal4DQMAnalyzer(const edm::ParameterSet& iConfig)
 :
  qie11digisToken_(consumes<QIE11DigiCollection>(iConfig.getUntrackedParameter<edm::InputTag>("tagQIE11", edm::InputTag("hcalDigis"))))
{
   //now do what ever initialization is needed
   hcalDbServiceToken_ = esConsumes<HcalDbService, HcalDbRecord>();

   usesResource("TFileService");
   edm::Service<TFileService> fs;

   hist3D_depth1 = fs->make<TH3I>("hist3D_depth1", "hist3D_depth1", 2000, 0, 2000, 64, -32, 32, 72, 0, 72);
   hist3D_depth2 = fs->make<TH3I>("hist3D_depth2", "hist3D_depth2", 2000, 0, 2000, 64, -32, 32, 72, 0, 72);
   hist3D_depth3 = fs->make<TH3I>("hist3D_depth3", "hist3D_depth3", 2000, 0, 2000, 64, -32, 32, 72, 0, 72);
   hist3D_depth4 = fs->make<TH3I>("hist3D_depth4", "hist3D_depth4", 2000, 0, 2000, 64, -32, 32, 72, 0, 72);
   hist3D_depth5 = fs->make<TH3I>("hist3D_depth5", "hist3D_depth5", 2000, 0, 2000, 64, -32, 32, 72, 0, 72);
   hist3D_depth6 = fs->make<TH3I>("hist3D_depth6", "hist3D_depth6", 2000, 0, 2000, 64, -32, 32, 72, 0, 72);
   hist3D_depth7 = fs->make<TH3I>("hist3D_depth7", "hist3D_depth7", 2000, 0, 2000, 64, -32, 32, 72, 0, 72);
   evttree = fs->make<TTree>("evttree", "evttree");
   evttree->Branch("RunNum", &RunNum);
   evttree->Branch("LumiSec", &LumiSec);

}


Hcal4DQMAnalyzer::~Hcal4DQMAnalyzer()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
Hcal4DQMAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  long runid   = iEvent.id().run();
  long eventid = iEvent.id().event();
  long lumiid  = iEvent.id().luminosityBlock();

  conditions = &iSetup.getData(hcalDbServiceToken_);

  edm::Handle<QIE11DigiCollection> qie11Digis;
  bool gotQIE11Digis = iEvent.getByToken(qie11digisToken_, qie11Digis);
  if (!gotQIE11Digis)
    std::cout << "Could not find HCAL QIE11Digis with tag: qie11Digis" << std::endl;

  for (QIE11DigiCollection::const_iterator it = qie11Digis->begin(); it != qie11Digis->end(); ++it) {
    const QIE11DataFrame digi = static_cast<const QIE11DataFrame>(*it);

    HcalDetId const& did = digi.detid();

    if(did.subdet() != HcalEndcap && did.subdet() != HcalBarrel) continue;

    const HcalQIECoder* channelCoder = conditions -> getHcalCoder(did);
    const HcalQIEShape* shape = conditions -> getHcalShape(channelCoder);
    HcalCoderDb coder(*channelCoder,*shape);
    CaloSamples cs; coder.adc2fC(digi,cs);

    float charge_ = 0.;
    for(int i=0; i<digi.samples(); i++){
      charge_ += cs[i];
    }

    if(charge_>20){
      if(did.depth()==1) hist3D_depth1->Fill(lumiid, did.ieta(), did.iphi());
      if(did.depth()==2) hist3D_depth2->Fill(lumiid, did.ieta(), did.iphi());
      if(did.depth()==3) hist3D_depth3->Fill(lumiid, did.ieta(), did.iphi());
      if(did.depth()==4) hist3D_depth4->Fill(lumiid, did.ieta(), did.iphi());
      if(did.depth()==5) hist3D_depth5->Fill(lumiid, did.ieta(), did.iphi());
      if(did.depth()==6) hist3D_depth6->Fill(lumiid, did.ieta(), did.iphi());
      if(did.depth()==7) hist3D_depth7->Fill(lumiid, did.ieta(), did.iphi());
    }
  }

  RunNum = runid;
  LumiSec = lumiid;
  evttree->Fill();

}


// ------------ method called once each job just before starting event loop  ------------
void
Hcal4DQMAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
Hcal4DQMAnalyzer::endJob()
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
Hcal4DQMAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

  //Specify that only 'tracks' is allowed
  //To use, remove the default given above and uncomment below
  //ParameterSetDescription desc;
  //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
  //descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(Hcal4DQMAnalyzer);
