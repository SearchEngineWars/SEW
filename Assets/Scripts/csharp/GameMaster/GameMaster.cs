using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameMaster : MonoBehaviour {

    /** Loader for handling all the data provided from json files */
    private DataLoader dataloader = new DataLoader();

    // Use this for initialization
    void Start () {
        dataloader.populateDataStructures();
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}
