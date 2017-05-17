using Newtonsoft.Json;
using System.Collections.Generic;
using System.IO;

public class DataLoader {

    // DATA_STRUCTURES_BEGIN
	List<events> listeventsEntries = new List<events>();
	List<Bonus> listBonusEntries = new List<Bonus>();
	List<CostBenefits> listCostBenefitsEntries = new List<CostBenefits>();
	List<Locations> listLocationsEntries = new List<Locations>();
	List<Technologies> listTechnologiesEntries = new List<Technologies>();
    // DATA_STRUCTURES_END

    public void populateDataStructures()
    {
        // BEGIN_READ_FILES
		List<string> eventsEntries = new List<string>(File.ReadAllLines("../csharp/dto/column/events.json"));
		List<string> bonusEntries = new List<string>(File.ReadAllLines("../csharp/dto/column/Bonus.json"));
		List<string> costbenefitsEntries = new List<string>(File.ReadAllLines("../csharp/dto/column/CostBenefits.json"));
		List<string> locationsEntries = new List<string>(File.ReadAllLines("../csharp/dto/column/Locations.json"));
		List<string> technologiesEntries = new List<string>(File.ReadAllLines("../csharp/dto/column/Technologies.json"));
        //END_READ_FILES
        // BEGIN_POPULATE_DATA_STRUCTS
		eventsEntries.ForEach(entry => listeventsEntries.Add(JsonConvert.DeserializeObject<events>(entry)));
		bonusEntries.ForEach(entry => listBonusEntries.Add(JsonConvert.DeserializeObject<Bonus>(entry)));
		costbenefitsEntries.ForEach(entry => listCostBenefitsEntries.Add(JsonConvert.DeserializeObject<CostBenefits>(entry)));
		locationsEntries.ForEach(entry => listLocationsEntries.Add(JsonConvert.DeserializeObject<Locations>(entry)));
		technologiesEntries.ForEach(entry => listTechnologiesEntries.Add(JsonConvert.DeserializeObject<Technologies>(entry)));
        // END_POPULATE_DATA_STRUCTS
    }
}













