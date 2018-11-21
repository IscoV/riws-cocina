import {Component, OnInit} from '@angular/core';
import {NgbCalendar, NgbDate} from '@ng-bootstrap/ng-bootstrap';
import {AppService} from './app.service';

interface Item {
    _score: number;
    _source: {
        name: string,
        description: string,
        categories: string[],
        steps: string[],
        dinners: number,
        ingredients: string[],
        difficulty: number,
        time: number,
        url: string,
        meal_type: string,
        tags: string[],
        language: string,
        last_update: string,
    };
}

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
    today: NgbDate;
    hoveredDate: NgbDate;
    fromDate: NgbDate;
    toDate: NgbDate;

    collapsed = true;
    page = 0;

    filter: { keywords?: string, dinners: number, difficulty: number, max_time?: any, last_update?: any } = {dinners: 1, difficulty: 5};
    found = {hits: [], total: 0};

    categories(item: Item) {
        item._source.categories.pop();
        return item._source.categories;
    }

    difficulty(item: Item) {
        switch (item._source.difficulty) {
            case 1:
                return 'Muy Fácil';
            case 2:
                return 'Fácil';
            case 3:
                return 'Medio';
            case 4:
                return 'Difícil';
            case 5:
                return 'Muy Difícil';
        }
    }

    difficultyClass(item: Item) {
        switch (item._source.difficulty) {
            case 1:
                return 'badge-success';
            case 2:
                return 'badge-info';
            case 3:
                return 'badge-secondary';
            case 4:
                return 'badge-warning';
            case 5:
                return 'badge-danger';
        }
    }

    constructor(calendar: NgbCalendar, public service: AppService) {
        this.today = calendar.getToday();
        this.fromDate = calendar.getPrev(calendar.getToday(), 'y', 1);
        this.toDate = calendar.getToday();
        this.filter.last_update = {from: this.fromDate, to: this.toDate};
    }

    ngOnInit(): void {
        this.filter.keywords = 'tortilla';
        this.search();
    }

    onDateSelection(date: NgbDate) {
        if (!this.fromDate && !this.toDate) {
            this.fromDate = date;
        } else if (this.fromDate && !this.toDate && date.after(this.fromDate)) {
            this.toDate = date;
        } else {
            this.toDate = null;
            this.fromDate = date;
        }
        this.filter.last_update = {from: this.fromDate, to: this.toDate};
    }

    isHovered(date: NgbDate) {
        return this.fromDate && !this.toDate && this.hoveredDate && date.after(this.fromDate) && date.before(this.hoveredDate);
    }

    isInside(date: NgbDate) {
        return date.after(this.fromDate) && date.before(this.toDate);
    }

    isRange(date: NgbDate) {
        return date.equals(this.fromDate) || date.equals(this.toDate) || this.isInside(date) || this.isHovered(date);
    }

    search() {
        this.service.get(this.filter, this.page).subscribe(
            (data: { hits: { hits: Item[], total: number } }) => this.found = data.hits
        );
    }

}
