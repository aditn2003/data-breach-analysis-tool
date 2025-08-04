const mongoose = require("mongoose");

const dataBreachSchema = new mongoose.Schema(
  {
    company: {
      name: { type: String, required: true, index: true },
      industry: { type: String, required: true },
      size: {
        type: String,
        enum: ["Small", "Medium", "Large", "Enterprise"],
        default: "Medium",
      },
      country: { type: String, required: true },
    },
    breach: {
      date: { type: Date, required: true },
      discoveryDate: { type: Date },
      recordsCompromised: { type: Number, required: true },
      dataTypes: [
        {
          type: String,
          enum: [
            "Personal Information",
            "Financial Data",
            "Health Records",
            "Login Credentials",
            "Payment Data",
            "Other",
          ],
        },
      ],
      breachType: {
        type: String,
        enum: [
          "Hacking",
          "Malware",
          "Phishing",
          "Insider Threat",
          "Physical Theft",
          "Accidental Exposure",
          "Other",
        ],
        required: true,
      },
      attackVector: {
        type: String,
        enum: [
          "Web Application",
          "Email",
          "Social Engineering",
          "Physical Access",
          "Third Party",
          "Unknown",
          "Other",
        ],
      },
    },
    impact: {
      financialLoss: { type: Number },
      customersAffected: { type: Number },
      regulatoryFines: { type: Number },
      reputationDamage: {
        type: String,
        enum: ["Low", "Medium", "High", "Critical"],
      },
    },
    response: {
      notificationDelay: { type: Number },
      lawEnforcementInvolved: { type: Boolean, default: false },
      creditMonitoring: { type: Boolean, default: false },
      insuranceCoverage: { type: Boolean, default: false },
    },
    technical: {
      encryptionStatus: {
        type: String,
        enum: ["Encrypted", "Unencrypted", "Partially Encrypted", "Unknown"],
      },
      securityMeasures: [String],
      vulnerabilityPatched: { type: Boolean, default: false },
      timeToDetect: { type: Number },
    },
    metadata: {
      source: { type: String, default: "Manual Entry" },
      verified: { type: Boolean, default: false },
      lastUpdated: { type: Date, default: Date.now },
      createdBy: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    },
  },
  {
    timestamps: true,
  }
);

dataBreachSchema.index({ "company.name": 1, "breach.date": -1 });
dataBreachSchema.index({ "breach.breachType": 1 });
dataBreachSchema.index({ "company.industry": 1 });
dataBreachSchema.index({ "breach.date": -1 });

dataBreachSchema.virtual("breachAge").get(function () {
  return Math.floor((Date.now() - this.breach.date) / (1000 * 60 * 60 * 24));
});

dataBreachSchema.virtual("severityScore").get(function () {
  let score = 0;

  if (this.breach.recordsCompromised > 1000000) score += 40;
  else if (this.breach.recordsCompromised > 100000) score += 30;
  else if (this.breach.recordsCompromised > 10000) score += 20;
  else if (this.breach.recordsCompromised > 1000) score += 10;

  if (this.impact.financialLoss > 10000000) score += 30;
  else if (this.impact.financialLoss > 1000000) score += 20;
  else if (this.impact.financialLoss > 100000) score += 10;

  if (this.impact.reputationDamage === "Critical") score += 20;
  else if (this.impact.reputationDamage === "High") score += 15;
  else if (this.impact.reputationDamage === "Medium") score += 10;

  return Math.min(score, 100);
});

const handleSubmit = async (e) => {
  e.preventDefault();

  const breachData = {
    company: {
      name: formData.companyName,
      industry: formData.industry,
      sector: formData.sector,
      size: formData.size,
    },
    breach: {
      name: formData.breachName,
      date: formData.date,
      description: formData.description,
      breachType: formData.breachType,
      source: formData.source,
    },
    impact: {
      recordsCompromised: parseInt(formData.recordsCompromised),
      dataTypes: formData.dataTypes.split(","),
    },
    response: {
      notificationDate: formData.notificationDate,
      regulatoryActions: formData.regulatoryActions,
    },
    technical: {
      attackVector: formData.attackVector,
      vulnerability: formData.vulnerability,
      mitigation: formData.mitigation,
    },
    metadata: {
      submittedBy: user?.username || "test",
    },
  };

  try {
    await axios.post("/breaches/new", breachData);
    alert("Breach submitted successfully!");
    setFormData(initialFormState);
  } catch (err) {
    console.error("Submission failed:", err.response?.data || err.message);
    alert("Submission failed!");
  }
};

module.exports = mongoose.model("DataBreach", dataBreachSchema);
