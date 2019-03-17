import { Router } from '@angular/router';
import { Component, OnInit, Input } from '@angular/core';
import { SearchingService } from '../searching-service.service';
import { browser } from 'protractor';

@Component({
  selector: 'app-input-search',
  templateUrl: './input-search.component.html',
  styleUrls: ['./input-search.component.css']
})
export class InputSearchComponent implements OnInit {

  searchingText: String;

  constructor(public Searching: SearchingService, private router: Router) { }

  ngOnInit() {
    this.searchingText = this.Searching.aim.what;
  }

  search() {
    console.log(this.router.url);
    this.router.navigate(['/result/' + this.searchingText + "/" + this.Searching.aim.browserType]);
  }

  setBrowserType(browserType: string) {
    console.log('browser type = ' + browserType);
    this.Searching.setBrowserType(browserType);
  }
}
