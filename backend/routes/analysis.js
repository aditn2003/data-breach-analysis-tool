const express = require("express");
const router = express.Router();
const { authenticateToken } = require("../middleware/auth");
const Analysis = require("../models/Analysis");
const DataBreach = require("../models/DataBreach");

router.get("/", authenticateToken, async (req, res) => {
  try {
    const analyses = await Analysis.find({ user: req.user.id })
      .populate("user", "name email")
      .sort({ createdAt: -1 });
    res.json(analyses);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.get("/:id", authenticateToken, async (req, res) => {
  try {
    const analysis = await Analysis.findById(req.params.id).populate(
      "user",
      "name email"
    );
    if (!analysis) {
      return res.status(404).json({ message: "Analysis not found" });
    }
    res.json(analysis);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.post("/", authenticateToken, async (req, res) => {
  try {
    const { analysisType, parameters, description } = req.body;

    const analysis = new Analysis({
      user: req.user.id,
      analysisType,
      parameters,
      description,
      status: "pending",
    });

    const savedAnalysis = await analysis.save();
    res.status(201).json(savedAnalysis);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

router.put("/:id/results", authenticateToken, async (req, res) => {
  try {
    const { results, status } = req.body;
    const analysis = await Analysis.findByIdAndUpdate(
      req.params.id,
      { results, status, completedAt: Date.now() },
      { new: true }
    );
    if (!analysis) {
      return res.status(404).json({ message: "Analysis not found" });
    }
    res.json(analysis);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

router.get("/trends/yearly", authenticateToken, async (req, res) => {
  try {
    const yearlyTrends = await DataBreach.aggregate([
      {
        $match: {
          date: { $type: "number" },
          recordsCompromised: { $type: "number" },
        },
      },
      {
        $group: {
          _id: "$date",
          breachCount: { $sum: 1 },
          totalRecords: { $sum: "$recordsCompromised" },
          avgRecords: { $avg: "$recordsCompromised" },
        },
      },
      {
        $project: {
          year: "$_id",
          breachCount: 1,
          totalRecords: 1,
          avgRecords: 1,
          _id: 0,
        },
      },
      { $sort: { year: 1 } },
    ]);

    res.json(yearlyTrends);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.get("/trends/by-type", authenticateToken, async (req, res) => {
  try {
    const typeAnalysis = await DataBreach.aggregate([
      {
        $group: {
          _id: "$breachType",
          count: { $sum: 1 },
          totalRecords: { $sum: "$recordsCompromised" },
          avgRecords: { $avg: "$recordsCompromised" },
        },
      },
      { $sort: { count: -1 } },
    ]);

    res.json(typeAnalysis);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.get("/trends/by-org", authenticateToken, async (req, res) => {
  try {
    const topOrgs = await DataBreach.aggregate([
      {
        $match: {
          recordsCompromised: { $type: "number" },
          organization: { $exists: true, $ne: null },
        },
      },
      {
        $group: {
          _id: "$organization",
          totalRecords: { $sum: "$recordsCompromised" },
        },
      },
      { $sort: { totalRecords: -1 } },
      { $limit: 10 },
    ]);

    res.json(topOrgs);
  } catch (err) {
    console.error("Top orgs error:", err);
    res.status(500).json({ message: "Failed to fetch top organizations" });
  }
});

const axios = require("axios");

router.post("/predictive", authenticateToken, async (req, res) => {
  try {
    const { organization, breachType, year } = req.body;

    const flaskResponse = await axios.post("http://localhost:5001/predict", {
      organization,
      breachType,
      year,
    });

    const prediction = flaskResponse.data;

    const analysis = new Analysis({
      user: req.user.id,
      analysisType: "predictive",
      parameters: { organization, breachType, year },
      results: prediction,
      status: "completed",
      completedAt: Date.now(),
    });

    const savedAnalysis = await analysis.save();
    res.json(savedAnalysis);
  } catch (error) {
    console.error("Prediction error:", error.message);
    res
      .status(500)
      .json({ message: "Failed to get prediction from ML service" });
  }
});

module.exports = router;
