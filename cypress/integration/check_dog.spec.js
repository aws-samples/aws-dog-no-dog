context("Check dog", function() {
  const pictures = [
    {fileName: "bigby.jpg", dog: true},
    {fileName: "masza.jpg", dog: true},
    {fileName: "masza2.jpg", dog: true},
    {fileName: "masza3.jpg", dog: true},
    {fileName: "masza4.jpg", dog: true},
    {fileName: "stella.jpg", dog: true},
    {fileName: "vyyhti.jpg", dog: true},
    {fileName: "wilbur.jpg", dog: true},
    {fileName: "no_dog.jpg", dog: false}
  ];

  pictures.forEach(picture => {
    it("Upload picture '"+ picture.fileName +"'", function() {
      cy.visit("/");

      const fileName = "../../pictures/"+picture.fileName;

      // Before upload
      cy.get("#image").should("not.exist");

      cy.get("#photo").should(($photo) => {
        expect($photo).to.have.length(1);
      });

      // Uploading picture
      cy.fixture(fileName)
        .then(fileContent => {
          cy.get("input#photo-select")
          .upload({fileContent, fileName, mimeType: "image/jpeg"});
        });

      // After upload
      cy.get("#photo .error").should("not.exist");

      // Check if the picture contains a dog or if the frontend is in 'mock'
      // mode. In 'mock' mode, all pictures return 'true', regardless of whether
      // they contain a dog or not.
      if(picture.dog || Cypress.env("mock")) {
        // Check if stamp has the right value
        cy.get("#image .stamp").should("exist");
        cy.get("#image .stamp").should("have.class", "stamp-dog");
        // Check if there is a label
        cy.get("#image .label").should("exist");
      } else {
        // Check if stamp has the right value
        cy.get("#image .stamp").should("exist");
        cy.get("#image .stamp").should("have.class", "stamp-nodog");
        // Check if there are no labels
        cy.get("#image .label").should("not.exist");
      }
    });
  });
});
