import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {ResultsService} from "../results.service";

@Component({
  selector: 'app-preview',
  templateUrl: './preview.component.html',
  styleUrls: ['./preview.component.css']
})
export class PreviewComponent implements OnInit {
    result = {content: '', updated_at: ''};


  constructor(private resultsService: ResultsService, private activatedRoute: ActivatedRoute) {}

  ngOnInit() {
        let pageID = this.activatedRoute.snapshot.paramMap.get('id');
        this.resultsService.getTorPreview(pageID)
          .subscribe(data => {
            if(data["result"]){
              this.result = data["result"];
            }
          });
  }

}
