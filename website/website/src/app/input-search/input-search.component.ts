import { Component, OnInit } from '@angular/core';
import { SearchingService } from "../searching-service.service";

@Component({
  selector: 'app-input-search',
  templateUrl: './input-search.component.html',
  styleUrls: ['./input-search.component.css']
})
export class InputSearchComponent implements OnInit {

  constructor(public Searching: SearchingService) { }

  ngOnInit() {
  }

  searchingText: String;

  search() {
    this.Searching.search(this.searchingText);
  }

}
