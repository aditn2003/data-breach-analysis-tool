const express = require("express");
const router = express.Router();
const { authenticateToken } = require("../middleware/auth");
const DataBreach = require("../models/DataBreach");

router.get("/", authenticateToken, async (req, res) => {
  try {
    const { page = 1, limit = 10, year, organization, breachType } = req.query;

    let query = {};

    if (year) query.year = year;
    if (organization)
      query.organization = { $regex: organization, $options: "i" };
    if (breachType) query.breachType = breachType;

    const breaches = await DataBreach.find(query)
      .limit(limit * 1)
      .skip((page - 1) * limit)
      .sort({ date: -1 });

    const total = await DataBreach.countDocuments(query);

    res.json({
      breaches,
      totalPages: Math.ceil(total / limit),
      currentPage: page,
      total,
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.get("/stats", authenticateToken, async (req, res) => {
  try {
    const stats = await DataBreach.aggregate([
      {
        $match: {
          recordsCompromised: { $type: "number" },
        },
      },
      {
        $group: {
          _id: null,
          totalBreaches: { $sum: 1 },
          totalRecords: { $sum: "$recordsCompromised" },
          avgRecords: { $avg: "$recordsCompromised" },
          maxRecords: { $max: "$recordsCompromised" },
        },
      },
    ]);

    const yearlyStats = await DataBreach.aggregate([
      {
        $match: {
          recordsCompromised: { $type: "number" },
        },
      },
      {
        $group: {
          _id: "$date",
          breachCount: { $sum: 1 },
          totalRecords: { $sum: "$recordsCompromised" },
        },
      },
      { $sort: { _id: 1 } },
    ]);

    const breachTypeStats = await DataBreach.aggregate([
      {
        $match: {
          recordsCompromised: { $type: "number" },
        },
      },
      {
        $group: {
          _id: "$breachType",
          count: { $sum: 1 },
          totalRecords: { $sum: "$recordsCompromised" },
        },
      },
    ]);

    const topIndustryAgg = await DataBreach.aggregate([
      {
        $match: {
          recordsCompromised: { $type: "number" },
          industry: { $exists: true, $ne: null, $ne: "" },
        },
      },
      {
        $group: {
          _id: "$industry",
          totalRecords: { $sum: "$recordsCompromised" },
          breachCount: { $sum: 1 },
        },
      },
      { $sort: { totalRecords: -1 } },
      { $limit: 1 },
    ]);
    const topIndustry = topIndustryAgg[0] || null;

    console.log("DEBUG topIndustry:", topIndustry);

    res.json({
      overall: stats[0] || {},
      yearly: yearlyStats,
      byType: breachTypeStats,
      topIndustry,
    });
  } catch (error) {
    console.error("Stats error:", error);
    res.status(500).json({ message: error.message });
  }
});

router.get("/:id", authenticateToken, async (req, res) => {
  try {
    const breach = await DataBreach.findById(req.params.id);
    if (!breach) {
      return res.status(404).json({ message: "Breach not found" });
    }
    res.json(breach);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.post("/", authenticateToken, async (req, res) => {
  try {
    const breach = new DataBreach(req.body);
    const savedBreach = await breach.save();
    res.status(201).json(savedBreach);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

router.put("/:id", authenticateToken, async (req, res) => {
  try {
    const breach = await DataBreach.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
    });
    if (!breach) {
      return res.status(404).json({ message: "Breach not found" });
    }
    res.json(breach);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

router.delete("/:id", authenticateToken, async (req, res) => {
  try {
    const breach = await DataBreach.findByIdAndDelete(req.params.id);
    if (!breach) {
      return res.status(404).json({ message: "Breach not found" });
    }
    res.json({ message: "Breach deleted successfully" });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;
