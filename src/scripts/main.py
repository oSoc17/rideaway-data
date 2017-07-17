import scraper, gfr_preprocessor, osm_processor, metadata

if __name__ == "__main__":
    scraper.scrape()
    gfr_preprocessor.preprocess()
    osm_processor.process_osm()
    metadata.check_metadata()
