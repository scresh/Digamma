import { Component, OnInit } from '@angular/core';
import { SearchingService } from "../searching-service.service";

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {

  constructor(public Searching: SearchingService) {
  }

  ngOnInit() {
  }

  changePage(numberPage){
    this.Searching.search(this.Searching.aim.what, numberPage);
  }

  previousPage(){
    if(this.Searching.aim.whichPage!=0)
      this.Searching.search(this.Searching.aim.what, this.Searching.aim.whichPage-1);
  }

  nextPage(){
    if(this.Searching.aim.whichPage!=this.Searching.lastPage)
      this.Searching.search(this.Searching.aim.what, this.Searching.aim.whichPage+1);
  }

}
