const mongoose = require("mongoose");

const analysisSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
    },
    type: {
      type: String,
      enum: [
        "trend_analysis",
        "risk_assessment",
        "prediction_model",
        "clustering",
        "anomaly_detection",
      ],
      required: true,
    },
    parameters: {
      dateRange: {
        start: { type: Date },
        end: { type: Date },
      },
      filters: {
        industries: [String],
        breachTypes: [String],
        countries: [String],
        minRecords: { type: Number },
        maxRecords: { type: Number },
      },
      modelConfig: {
        algorithm: { type: String },
        hyperparameters: mongoose.Schema.Types.Mixed,
        features: [String],
      },
    },
    results: {
      summary: {
        totalBreaches: { type: Number },
        totalRecords: { type: Number },
        averageSeverity: { type: Number },
        topIndustries: [String],
        topBreachTypes: [String],
      },
      predictions: [
        {
          date: { type: Date },
          predictedValue: { type: Number },
          confidence: { type: Number },
          actualValue: { type: Number },
        },
      ],
      trends: [
        {
          period: { type: String },
          metric: { type: String },
          value: { type: Number },
          change: { type: Number },
        },
      ],
      clusters: [
        {
          clusterId: { type: Number },
          center: mongoose.Schema.Types.Mixed,
          members: [
            { type: mongoose.Schema.Types.ObjectId, ref: "DataBreach" },
          ],
          characteristics: mongoose.Schema.Types.Mixed,
        },
      ],
      riskScores: [
        {
          company: { type: String },
          industry: { type: String },
          riskScore: { type: Number },
          factors: [String],
        },
      ],
    },
    performance: {
      accuracy: { type: Number },
      precision: { type: Number },
      recall: { type: Number },
      f1Score: { type: Number },
      mse: { type: Number },
      mae: { type: Number },
    },
    metadata: {
      createdBy: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "User",
        required: true,
      },
      status: {
        type: String,
        enum: ["pending", "processing", "completed", "failed"],
        default: "pending",
      },
      processingTime: { type: Number },
      dataPoints: { type: Number },
      lastUpdated: { type: Date, default: Date.now },
    },
  },
  {
    timestamps: true,
  }
);

analysisSchema.index({ "metadata.createdBy": 1, createdAt: -1 });
analysisSchema.index({ type: 1 });
analysisSchema.index({ "metadata.status": 1 });

analysisSchema.virtual("analysisAge").get(function () {
  return Math.floor((Date.now() - this.createdAt) / (1000 * 60 * 60 * 24));
});

module.exports = mongoose.model("Analysis", analysisSchema);
